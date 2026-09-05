from typing import Callable, Unpack

from .component import Component

# A layout takes the app title followed by any number of page components:
# layout(title, *children) -> Component
PageLayoutFunc = Callable[[str, Unpack[tuple[Component, ...]]], Component]


def DefaultPageLayout(title: str, *args: Component) -> Component:
    return Component(
        "html",
        Component(
            "head",
            Component("title", title),
            Component(
                "script", src="https://unpkg.com/htmx.org@4.0.0/dist/htmx.min.js"
            ),
            # hx-sse extension: makes htmx treat text/event-stream responses
            # (and hx-sse:connect elements) as Server-Sent Events streams.
            Component(
                "script",
                src="https://unpkg.com/htmx.org@4.0.0/dist/ext/hx-sse.min.js",
            ),
        ),
        Component(
            "body",
            *args,
            style={
                "padding": "4rem",
                "background-color": "oklch(98.5% 0.002 247.839)",
                "color": "oklch(21% 0.034 264.665)",
            },
        ),
    )
