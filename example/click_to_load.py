#!/usr/bin/env -S uv run --script
#
# "Click to Load" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/click-to-load
#
# A "Show more comments" button sits at the end of a list. Clicking it
# fetches the next page, which is the next batch of comments plus (if any
# remain) a new button that replaces itself via hx-swap="outerHTML".
# No client-side state: pagination lives entirely in the server response.
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
from heflex.component import Button, Component, Div, Strong
from heflex import Heflex

PAGE_SIZE = 3
TOTAL_COMMENTS = 12

comments = [f"Comment #{i}: {'x' * (i % 5 + 1)} — something said in reply." for i in range(1, TOTAL_COMMENTS + 1)]


def render_comments(start: int, end: int) -> list[Component]:
    return [
        Div(Strong(c), style={"border": "1px solid #ccc", "padding": "0.5rem", "margin-bottom": "0.5rem"})
        for c in comments[start:end]
    ]


def more_button(page: int) -> Component:
    return Button(
        "Show more comments",
        hx_get=f"/comments?page={page}",
        hx_swap="outerHTML",
        hx_target="this",
        style={"background-color": "oklch(54.6% 0.245 262.881)", "color": "white", "border-radius": "4px"},
    )


hx = Heflex(FastAPI(debug=True, title="Click to Load"))


@hx.route("/", methods=["GET"])
async def index() -> list[Component]:
    """Initial page: first batch plus the button for the next page."""
    return [Div(*render_comments(0, PAGE_SIZE), more_button(page=2))]


@hx.route("/comments", methods=["GET"])
async def comments_page(page: int = Query(1)) -> list[Component]:
    """
    Next items plus a button pointing one page further. When there are no
    more pages the button is simply omitted, so the chain ends.
    """
    start = (page - 1) * PAGE_SIZE
    batch = render_comments(start, start + PAGE_SIZE)
    if start + PAGE_SIZE < TOTAL_COMMENTS:
        batch.append(more_button(page=page + 1))
    return batch


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
