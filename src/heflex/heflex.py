#!/usr/bin/env python3

import functools
import inspect
from dataclasses import dataclass, field
from typing import Callable, List, Optional

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse, StreamingResponse

from .component import Component
from .default_page_layout import DefaultPageLayout, PageLayoutFunc
from .sse import frame_item


@dataclass
class Heflex:
    app: FastAPI = field(default_factory=FastAPI)
    page_layout: PageLayoutFunc = DefaultPageLayout

    def route(self, path: str, methods: List[str] = ["GET"], **kwargs):
        def decorator(func: Callable[..., Component]):
            if inspect.isgeneratorfunction(func):
                raise TypeError(
                    f"Route '{path}' handler must not be a sync generator; heflex "
                    "renders Component return values. Return a list of Components, "
                    "or pass through a Response (e.g. StreamingResponse). Use an "
                    "async generator to stream SSE (text/event-stream)."
                )
            # Async generators are the first-class SSE path: each yielded
            # Component/str/RawHTML/SSEEvent is framed as one SSE message.
            is_sse = inspect.isasyncgenfunction(func)
            sig = inspect.signature(func)
            params = list(sig.parameters.values())

            has_request = any(
                p.annotation is Request or p.name == "request" for p in params
            )
            request_idx = next(
                (
                    i
                    for i, p in enumerate(params)
                    if p.annotation is Request or p.name == "request"
                ),
                None,
            )

            # Ensure the signature carries a parameter for the FastAPI request.
            # Inject it at index 0: appending an un-defaulted param after
            # defaulted ones (e.g. Query(...) defaults) makes sig.replace()
            # raise 'non-default argument follows default argument'.
            if request_idx is None:
                request_idx = 0
                new_param = inspect.Parameter(
                    "request",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                )
                params.insert(request_idx, new_param)
            setattr(func, "__signature__", sig.replace(parameters=params))

            @functools.wraps(func)
            async def htmx_handler(*args, **fn_kwargs):
                request: Request | None = fn_kwargs.get("request")
                if not request:
                    request = next((a for a in args if isinstance(a, Request)), None)

                call_kwargs = fn_kwargs.copy()
                if not has_request and "request" in call_kwargs:
                    del call_kwargs["request"]

                if is_sse:

                    async def sse_stream():
                        agen = func(*args, **call_kwargs)
                        async for item in agen:
                            yield frame_item(item).encode()

                    return StreamingResponse(
                        sse_stream(), media_type="text/event-stream"
                    )

                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **call_kwargs)
                else:
                    result = func(*args, **call_kwargs)

                if isinstance(result, Response):
                    # Explicit response (e.g., RedirectResponse) passes through.
                    return result
                if isinstance(result, Component):
                    results: list[Component] = [result]
                elif inspect.isasyncgen(result):
                    # Returning an async generator object is equivalent to
                    # being one; stream it as SSE.

                    async def sse_stream_returned():
                        async for item in result:
                            yield frame_item(item).encode()

                    return StreamingResponse(
                        sse_stream_returned(), media_type="text/event-stream"
                    )
                elif inspect.isgenerator(result):
                    raise ValueError(
                        f"Route '{path}' returned a sync generator; heflex renders "
                        "Component return values. Use an async generator to stream "
                        "SSE (text/event-stream), or pass through a Response."
                    )
                else:
                    try:
                        items: Optional[list[object]] = list(result)
                    except TypeError:
                        items = None
                    # An empty list is valid: it renders an empty fragment.
                    if items is None or not all(
                        isinstance(r, Component) for r in items
                    ):
                        raise ValueError(
                            f"Route '{path}' returned {type(result).__name__}; "
                            "a route must return a Component, an iterable of "
                            "Components, or a Response (e.g., RedirectResponse)"
                        )
                    results: list[Component] = items  # type: ignore[assignment]

                is_htmx = request and request.headers.get("HX-Request") == "true"

                if is_htmx:
                    return HTMLResponse(content="".join(r.render() for r in results))
                full_page = self.page_layout(self.app.title, *results)
                # The layout returns the <html> element; the doctype is
                # prepended here so browsers don't fall back to quirks mode.
                return HTMLResponse(content=f"<!DOCTYPE html>\n{full_page.render()}")

            setattr(htmx_handler, "__signature__", sig.replace(parameters=params))
            # functools.wraps links __wrapped__ back to the user function;
            # FastAPI follows that chain and would route an async-generator
            # handler through its native streaming path (calling htmx_handler
            # without awaiting it). The explicit __signature__ above is all
            # dependency resolution needs, so sever the link.
            setattr(htmx_handler, "__wrapped__", None)

            self.app.api_route(path, methods=methods, **kwargs)(htmx_handler)

            return func

        return decorator
