#!/usr/bin/env python3

from typing import Annotated
from pathlib import Path
from fastapi import FastAPI, Request
from fastapi import Form as FastAPIForm
from heflex import Button, Component, Div, Heflex, Script, Form, Input, Style

current_file_path = Path(__file__).resolve()

sortable_js = current_file_path.parent / "htmx_example_sortable.js"

style = """
.zz-sortable-item {
  border: 1px solid #DEDEDE;
  padding: 12px;
  margin: 8px;
  width: 200px;
  cursor: grab;
}
"""


def page_layout(title: str, *args: Component):
    return Component(
        "html",
        Component(
            "head",
            Component("title", title),
            Script("", src="https://unpkg.com/htmx.org@4.0.0/dist/htmx.min.js"),
            Style(style),
        ),
        Component("body", *args),
        Script(
            "",
            src="https://cdn.jsdelivr.net/npm/sortablejs@latest/Sortable.min.js",
        ),
        Script(sortable_js.read_text()),
    )


hx = Heflex(FastAPI(title="Sortable", debug=True), page_layout=page_layout)

order = ["1", "2", "3", "4", "5"]


def items_components() -> list[Component]:
    divs = []
    for num in order:
        divs.append(
            Div(
                Input(value=num, name="item", type="hidden"),
                f"Item {num}",
                class_="zz-sortable-item",
            )
        )
    return divs


@hx.route("/")
async def home() -> Component:

    divs = items_components()
    return Form(
        Div("Updating...", class_="htmx-indicator"),
        *divs,
        class_="sortable",
        hx_post="/items",
        hx_trigger="end",
    )


@hx.route("/items", methods=["POST"])
async def items(item: Annotated[list[str], FastAPIForm()]):
    global order
    order = item
    return items_components()


app = hx.app
