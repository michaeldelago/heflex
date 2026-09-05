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
    page_layout: PageLayoutFunc = field(default_factory=lambda: DefaultPageLayout)

    def route(self, path: str, methods: List[str] = ["GET"], **kwargs):
        def decorator(func: Callable[..., Component]):
            sig = inspect.signature(func)
            params = list(sig.parameters.values())

            has_request = any(
                p.annotation == Request or p.name == "request" for p in params
            )

            # stupid hack to ensure there's a parameter for the fastapi request
            if not has_request:
                new_param = inspect.Parameter(
                    "request",
                    inspect.Parameter.POSITIONAL_OR_KEYWORD,
                    annotation=Request,
                )
                params.append(new_param)
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

                if isinstance(result, Component):
                    results: list[Component] = [result]
                elif (
                    isinstance(result, Iterable)
                    and len(result) > 0
                    and isinstance(result[0], Component)
                ):
                    results: list[Component] = [r for r in result]
                else:
                    return result

                is_htmx = request and request.headers.get("HX-Request") == "true"

                if is_htmx:
                    return HTMLResponse(content="".join(r.render() for r in results))
                full_page = self.page_layout(self.app.title, *results)
                return HTMLResponse(content=full_page.render())

            if hasattr(htmx_handler, "__signature__"):
                setattr(htmx_handler, "__signature__", sig.replace(parameters=params))

            self.app.api_route(path, methods=methods, **kwargs)(htmx_handler)

            return func

        return decorator
