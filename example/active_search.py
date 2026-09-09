#!/usr/bin/env -S uv run --script
#
# "Active Search" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/active-search
#
# A search input targets a results <tbody>. Its hx-trigger combines three
# triggers: "input changed delay:200ms" (debounced keystrokes, ignoring
# keys that don't change the value), keyup[key=='Enter'] (send immediately
# on Enter via an event filter), and load (populate the table on page
# load). hx-indicator shows a loading spinner while a request is in flight.
# The server responds with matching table rows for the #results target.
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
from heflex import Component, Div, Heflex, Input, Style
from heflex.component import H1, Span, Table, Tbody, Td, Tr

PEOPLE = [
    ("Venus Grimes", "venus.grimes@example.com"),
    ("Fletcher Owen", "fletcher.owen@example.com"),
    ("Mara Quinn", "mara.quinn@example.com"),
    ("Devon Park", "devon.park@example.com"),
]


def result_rows(q: str) -> list[Component]:
    """Matching rows; the response is swapped into the #results tbody."""
    q = q.strip().lower()
    matches = [(name, email) for name, email in PEOPLE if q == "" or q in name.lower() or q in email.lower()]
    if not matches:
        return [Tr(Td("No matches.", **{"colspan": 2}))]
    return [Tr(Td(name), Td(email)) for name, email in matches]


hx = Heflex(FastAPI(debug=True, title="Active Search"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("People"),
        Input(
            type="search",
            name="q",
            placeholder="Search name or email…",
            hx_post="/search",
            hx_trigger="input changed delay:200ms, keyup[key=='Enter'], load",
            hx_target="#results",
            hx_indicator="#loading",
        ),
        Span("Searching...", id="loading", class_="htmx-indicator"),
        Table(
            Tbody(id="results"),
            style={"border-collapse": "collapse"},
        ),
        Style(
            """
            .htmx-indicator { display: none; }
            .htmx-request .htmx-indicator, .htmx-request.htmx-indicator { display: inline; }
            table td { border: 1px solid #ccc; padding: 0.4rem; }
            """
        ),
    )


@hx.route("/search", methods=["POST"])
async def search(q: str = Query("")) -> list[Component]:
    return result_rows(q)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
