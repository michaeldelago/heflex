#!/usr/bin/env -S uv run --script
#
# "Dialogs" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/dialogs
#
# Uses the native <dialog> element — the browser provides the backdrop, focus
# trap, Escape-to-close and correct top-layer stacking; no JavaScript. The open
# button uses command="show-modal" + commandfor="#modal" (command="close"
# closes), closedby="any" also dismisses on backdrop click or Escape. Adding
# hx-get + hx-target="#modal-body" to the SAME button fetches the content and
# opens the dialog in one click — the dialog opens instantly so the user sees
# the loading state, then the content replaces it. Notes: for yes/no questions
# hx-confirm is enough (no dialog); collect values with the hx-prompt extension;
# if a CSS reset kills the centering, restore `dialog:modal { margin: auto }`.
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uvicorn
from fastapi import FastAPI
from heflex.component import Button, Component, Dialog, Div, H1, H2, P, Style, Table, Td, Th, Tr
from heflex import Heflex


def modal() -> Component:
    return Dialog(
        H2("Report"),
        # Loading state until the hx-get from the open button lands.
        Div("Loading…", id="modal-body"),
        Button("Close", type="button", command="close", style={"margin-top": "1rem"}),
        id="modal",
        closedby="any",
    )


hx = Heflex(FastAPI(debug=True, title="Dialogs"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Dialogs"),
        Button(
            "Open a Modal",
            type="button",
            command="show-modal",
            commandfor="#modal",
            hx_get="/report",
            hx_target="#modal-body",
        ),
        modal(),
        Style(
            """
            dialog:modal { margin: auto; padding: 1.5rem; border: none; box-shadow: 0 0 2rem rgb(0 0 0 / 0.3); }
            dialog::backdrop { background: rgb(0 0 0 / 0.5); }
            """
        ),
    )


@hx.route("/report", methods=["GET"])
async def report() -> Component:
    """Content swapped into #modal-body once fetched."""
    return Div(
        P("Here is your report:"),
        Table(
            Tr(*(Th(h) for h in ("Region", "Sales"))),
            Tr(Td("North"), Td("$12,400")),
            Tr(Td("South"), Td("$9,800")),
            style={"border-collapse": "collapse"},
        ),
    )


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
