#!/usr/bin/env python3

import functools
import inspect
from dataclasses import dataclass, field
from typing import Callable, Coroutine, List, Optional, Iterable

from fastapi import FastAPI, Request, Response
from fastapi.responses import HTMLResponse

from .component import Component
from .default_page_layout import DefaultPageLayout, PageLayoutFunc


@dataclass
class Heflex:
    app: FastAPI = field(default_factory=FastAPI)
    page_layout: PageLayoutFunc = DefaultPageLayout

    def route(self, path: str, methods: List[str] = ["GET"], **kwargs):
        def decorator(func: Callable[..., Component]):
            if inspect.isgeneratorfunction(func) or inspect.isasyncgenfunction(func):
                raise TypeError(
                    f"Route '{path}' handler must not be a generator; heflex renders "
                    "Component return values. Return a list of Components instead, "
                    "or pass through a Response (e.g. StreamingResponse)."
                )
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

                if inspect.iscoroutinefunction(func):
                    result = await func(*args, **call_kwargs)
                else:
                    result = func(*args, **call_kwargs)

                if isinstance(result, Response):
                    # Explicit response (e.g., RedirectResponse) passes through.
                    return result
                if isinstance(result, Component):
                    results: list[Component] = [result]
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

            if hasattr(htmx_handler, "__signature__"):
                setattr(htmx_handler, "__signature__", sig.replace(parameters=params))

            self.app.api_route(path, methods=methods, **kwargs)(htmx_handler)

            return func

        return decorator
