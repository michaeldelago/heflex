#!/usr/bin/env -S uv run --script
#
# "Keyboard Shortcuts" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/keyboard-shortcuts
#
# A keyboard event joins click in hx-trigger (comma-separated events). The
# event filter keyup[altKey&&shiftKey&&code=='KeyD'] matches only the
# Alt+Shift+D combo, and from:body moves the listener to <body> so the shortcut
# is global, not just when the button is focused. The server responds with the
# result content, exactly like a click would. Notes: use `code` (physical key,
# layout independent), not `key` (produced character) — use key only when you
# want the character (key=='?'); the filter expression has access to the raw
# KeyboardEvent properties (key, code, altKey, ctrlKey, shiftKey, metaKey);
# test in every browser/OS since combos like Ctrl+W reach the browser first.
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
from heflex import Button, Component, Div, Heflex, Style

COUNT = {"done": 0}

TRIGGER = "click, from:body keyup[altKey&&shiftKey&&code=='KeyD']"


hx = Heflex(FastAPI(debug=True, title="Keyboard Shortcuts"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        Component("h1", "Keyboard shortcuts"),
        Button(
            "Do It! (Alt+Shift+D)",
            type="button",
            hx_post="/do",
            hx_trigger=TRIGGER,
            hx_target="#result",
            hx_swap="innerHTML",
        ),
        Div(
            "Click the button or press Alt+Shift+D anywhere on the page…",
            id="result",
            style={"margin-top": "0.75rem", "padding": "0.75rem", "border": "1px solid #ccc"},
        ),
    )


@hx.route("/do", methods=["POST"])
async def do_it() -> Component:
    """Result content, identical whether triggered by click or shortcut."""
    COUNT["done"] += 1
    return Div(f"Done! (times done: {COUNT['done']})", class_="done")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
