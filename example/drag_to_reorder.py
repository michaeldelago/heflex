#!/usr/bin/env -S uv run --script
#
# "Drag to Reorder" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/drag-to-reorder
#
# Integrates Sortable.js with htmx: items are wrapped in a form that POSTs the
# new order on Sortable's `end` event (it bubbles up to the form). Each item
# carries a hidden input so the server receives the ids in their new order, and
# an .htmx-indicator shows while the request is in flight. hx-on:load builds
# the Sortable instance when htmx processes the form. A custom page layout is
# used to load both htmx and Sortable.js from CDNs (DefaultPageLayout only loads
# htmx).
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uvicorn
from fastapi import FastAPI, Form as FastAPIForm
from heflex import (
    Component,
    DefaultPageLayout,  # noqa: F401  (not used — custom layout below loads Sortable.js too)
    Div,
    Heflex,
    Input,
    Script,
    Style,
)
from heflex.component import Body, Form, H1, Head, Html, Title

ITEMS = ["Item 1", "Item 2", "Item 3", "Item 4"]


def page(title: str, content: Component) -> Component:
    """DefaultPageLayout plus the Sortable.js CDN script."""
    return Html(
        Head(
            Title(title),
            Script("", src="https://unpkg.com/htmx.org@4.0.0/dist/htmx.min.js"),
            Script("", src="https://cdn.jsdelivr.net/npm/sortablejs@1.15.6/Sortable.min.js"),
        ),
        Body(
            content,
            style={"padding": "4rem", "background-color": "oklch(98.5% 0.002 247.839)", "color": "oklch(21% 0.034 264.665)"},
        ),
    )


def item_list() -> Div:
    return Div(
        *(Div(Input(type="hidden", name="ids", value=i), i, class_="item") for i in ITEMS),
        id="list",
        style={"max-width": "20rem"},
    )


hx = Heflex(FastAPI(debug=True, title="Drag to Reorder"), page_layout=page)


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Drag to reorder"),
        Form(
            Div("Updating...", class_="htmx-indicator", style={"display": "none"}),
            item_list(),
            hx_post="/items",
            hx_trigger="end",
            **{"hx-on:load": "Sortable.create(this.querySelector('#list'), { animation: 150 });"},
        ),
        Style(
            """
            .item { border: 1px solid #ccc; padding: 0.5rem; margin-bottom: 0.4rem; background: white; }
            .sortable-ghost { opacity: 0.4; }
            .htmx-request .htmx-indicator, .htmx-request.htmx-indicator { display: inline; }
            """
        ),
    )


@hx.route("/items", methods=["POST"])
async def items(ids: list[str] = FastAPIForm([])) -> Component:
    """Reorder the in-memory list to match the submitted id order."""
    global ITEMS
    by_id = {v: v for v in ITEMS}
    new_order = [v for i in ids if (v := by_id.get(i))]
    # Keep any ids the client didn't submit at the end (defensive).
    new_order += [v for v in ITEMS if v not in new_order]
    if new_order and new_order != ITEMS:
        ITEMS = new_order
        return Div("Order saved.", class_="flash")
    return Div("", class_="flash")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
