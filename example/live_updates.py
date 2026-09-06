#!/usr/bin/env -S uv run --script
#
# "Live Updates" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/live-updates
#
# The server holds the SSE connection open and pushes a row whenever a price
# moves; hx-sse:connect opens it on load and keeps it alive for as long as the
# page is on screen. sse.releaseOn:end (the default here) keeps the request
# open until the stream ends, so the htmx-request class stays on the connection
# element and its htmx-indicator badge stays lit. Each push is an OOB partial —
# a row with hx-swap-oob that targets exactly the row it updates; a partial's
# target is an ordinary selector, so one connection can update any part of the
# page. Over plain hx-get streaming (see LLM Streaming), hx-sse:connect adds
# backoff reconnection and background-tab pausing for long-lived connections;
# the server can close it with a named event, and it closes when the element
# leaves the DOM. heflex note: an async-generator handler that yields forever
# IS a live connection — uvicorn cancels it on client disconnect.
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import asyncio
import random

import uvicorn
from fastapi import FastAPI
from heflex import Component, Div, Heflex, Style

SYMBOLS = {"HTMX": 142.10, "REST": 88.45, "FLEX": 17.62}


def ticker_table() -> Component:
    return Component(
        "table",
        Component("thead", Component("tr", Component("th", "Symbol"), Component("th", "Price"))),
        Component(
            "tbody",
            *(
                Component(
                    "tr",
                    Component("td", symbol),
                    Component("td", f"{price:.2f}"),
                    id=f"row-{symbol}",
                )
                for symbol, price in SYMBOLS.items()
            ),
        ),
        style={"border-collapse": "collapse"},
    )


hx = Heflex(FastAPI(debug=True, title="Live Updates"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        Component("h1", "Live prices"),
        # Connection element: opens on load, badge lit for the whole stream.
        Component(
            "span",
            "Live",
            id="live-badge",
            class_="htmx-indicator",
            **{"hx-sse:connect": "/prices"},
        ),
        ticker_table(),
        Style(
            """
            .htmx-indicator { display: none; color: #080; font-size: 0.8rem; }
            htmx-request .htmx-indicator, htmx-request.htmx-indicator { display: inline; }
            """
        ),
    )


@hx.route("/prices", methods=["GET"])
async def prices() -> object:
    """Infinite stream: one OOB row partial per simulated price move."""
    while True:
        symbol = random.choice(list(SYMBOLS))
        SYMBOLS[symbol] = max(0.01, SYMBOLS[symbol] + random.uniform(-2.5, 2.5))
        yield Component(
            "tr",
            Component("td", symbol),
            Component("td", f"{SYMBOLS[symbol]:.2f}"),
            hx_swap_oob="true",
            id=f"row-{symbol}",
        )
        await asyncio.sleep(1.0)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
