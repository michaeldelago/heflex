#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///


import asyncio

import uvicorn
from fastapi import FastAPI
from heflex import Button, Component, Div, Heflex, SSEEvent

hx = Heflex(FastAPI(debug=True, title="SSE Ticker"))


@hx.route("/", methods=["GET"])
async def home():
    """
    Two SSE demos:

    1. Streamed update — clicking "Generate" makes an htmx request that is
       answered with text/event-stream; each unnamed event's payload is
       appended to <output> (hx-swap="beforeend").
    2. Persistent connection — after clicking "Connect", hx-sse:connect opens
       a GET /ticker stream; each tick replaces the #display element until the
       server sends the named `done` event, which closes via hx-sse:close.
    """
    return Div(
        Div(
            Button(
                "Generate",
                hx_get="/greeting",
                hx_target="#output",
                hx_swap="beforeend",
            ),
            Component("output", id="output"),
        ),
        Div(
            Button("Connect", id="connect"),
            Div(
                hx_trigger="click from:#connect",
                hx_swap="none",
                **{"hx-sse:connect": "/ticker", "hx-sse:close": "done"},
            ),
            Component("h2", "waiting to connect…", id="display"),
        ),
    )


@hx.route("/greeting", methods=["GET"])
async def greeting():
    """Stream a message chunk by chunk (the LLM-token pattern)."""
    for chunk in ["Hello", ", ", "world", "!"]:
        yield chunk
        await asyncio.sleep(0.2)


@hx.route("/ticker", methods=["GET"])
async def ticker():
    """Persistent SSE connection: ticks, then a named event to close."""
    for i in range(1, 4):
        yield Component("h2", f"tick {i}")
        await asyncio.sleep(0.8)
    yield SSEEvent(event="done", data="")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
