#!/usr/bin/env -S uv run --script
#
# "Linked Selects" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/linked-selects
#
# The first select requests new options whenever its value changes (htmx
# defaults to the change trigger for selects, so no hx-trigger is needed):
# hx-get requests /models with the current make as a query parameter,
# hx-target="#models" swaps the response into the second select, and
# hx-indicator shows a loading message while in flight. The server responds
# with <option> elements.
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uvicorn
from fastapi import FastAPI, Query
from heflex.component import Component, Div, H1, Option, Select, Span, Style
from heflex import Heflex

CARS = {
    "Toyota": ["Corolla", "Camry", "RAV4"],
    "Honda": ["Civic", "Accord", "CR-V"],
    "Volkswagen": ["Golf", "Passat", "Tiguan"],
}


def option(value: str) -> Component:
    return Option(value, value=value)


hx = Heflex(FastAPI(debug=True, title="Linked Selects"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Cars"),
        Select(
            Option("", value=""),
            *(option(m) for m in CARS),
            name="make",
            hx_get="/models",
            hx_target="#models",
            hx_indicator="#models-indicator",
        ),
        Span("Loading...", id="models-indicator", class_="htmx-indicator"),
        Select(Option("", value=""), name="model", id="models"),
        Style(
            """
            .htmx-indicator { display: none; }
            .htmx-request .htmx-indicator, .htmx-request.htmx-indicator { display: inline; }
            """
        ),
    )


@hx.route("/models", methods=["GET"])
async def models(make: str = Query("")) -> list[Component]:
    """Options for the selected make; swapped into #models."""
    if make not in CARS:
        return [option("")]
    return [option(m) for m in CARS[make]]


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
