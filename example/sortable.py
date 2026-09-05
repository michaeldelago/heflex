#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

from pathlib import Path
from typing import Annotated

import uvicorn
from fastapi import FastAPI
from fastapi import Form as FastAPIForm
from heflex import Component, Div, Form, Heflex, Input, Script, Style

current_file_path = Path(__file__).resolve()

sortable_js = """
htmx.config.logAll = true;

htmx.onLoad(function (content) {
    var sortables = content.querySelectorAll(".sortable");
    for (var i = 0; i < sortables.length; i++) {
        var sortable = sortables[i];
        var sortableInstance = new Sortable(sortable, {
            animation: 150,
            ghostClass: "blue-background-class",

            // Make the `.htmx-indicator` unsortable
            filter: ".htmx-indicator",
            onMove: function (evt) {
                return evt.related.className.indexOf("htmx-indicator") === -1;
            },

            // Disable sorting on the `end` event
            onEnd: function (evt) {
                this.option("disabled", true);
            },
        });

        // Re-enable sorting on the `htmx:afterSwap` event
        sortable.addEventListener("htmx:after:swap", function () {
            console.log("enabled");
            sortableInstance.option("disabled", false);
        });
    }
});
"""

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
        Script(sortable_js),
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

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
