from typing import Callable, Iterable

from heflex.component import Component

PageLayoutFunc = Callable[[str, Component], Component]


def DefaultPageLayout(title: str, *args: Component) -> Component:
    return Component(
        "html",
        Component(
            "head",
            Component("title", title),
            Component(
                "script", src="https://unpkg.com/htmx.org@4.0.0/dist/htmx.min.js"
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
