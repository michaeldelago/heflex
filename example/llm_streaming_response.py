#!/usr/bin/env -S uv run --script
#
# "LLM Streaming Response" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/llm-streaming-response
#
# A (fake) model answers token by token over an SSE response; the hx-sse
# extension takes over any text/event-stream response, so a normal form POST is
# all that is needed — no hx-sse:connect. The request lives on the form and
# targets #transcript with hx-swap="beforeend scroll:bottom", so each event
# appends (the question lands as a block, tokens flow after it).
# hx-disable="find fieldset" disables the prompt and Ask button until the reply
# finishes — SSE defaults to sse.releaseOn:end. Clear sits outside the fieldset
# so it stays available; the server stops the in-flight generation and answers
# with an empty body, which empties the transcript (one source of truth).
# heflex note: async-generator handlers ARE this pattern — each yielded item is
# one unnamed SSE event.
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
from fastapi import FastAPI, Form as FastAPIForm
from heflex.component import Button, Component, Div, Fieldset, H1, Input, RawHTML, Style
from heflex import Heflex

# One source of truth for in-flight generation; /clear cancels it server-side.
GENERATION = {"active": False}


def fake_model_answer(prompt: str) -> list[str]:
    """A canned answer split into token-ish chunks, as a real LLM would emit."""
    text = (
        f"About “{prompt.strip()}”: hypermedia is data in which each item "
        "carries the links to related items. The client follows them instead "
        "of hard-coding endpoints — that is HATEOAS in practice."
    )
    return [w + " " for w in text.split()]


hx = Heflex(FastAPI(debug=True, title="LLM Streaming"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Ask the model"),
        # Transcript is appended to (beforeend), and scroll keeps tokens in view.
        Div(
            id="transcript",
            style={
                "min-height": "8rem",
                "border": "1px solid #ccc",
                "padding": "0.75rem",
                "margin-bottom": "1rem",
                "max-height": "16rem",
                "overflow-y": "auto",
            },
        ),
        Fieldset(
            Input(
                type="text",
                name="prompt",
                placeholder="Ask something…",
                style={"width": "24rem"},
            ),
            Button("Ask", type="submit"),
            hx_post="/ask",
            hx_target="#transcript",
            hx_swap="beforeend scroll:bottom",
        ),
        Div(
            Button(
                "Clear",
                type="button",
                hx_post="/clear",
                hx_target="#transcript",
                hx_swap="innerHTML",
            ),
            style={"margin-top": "0.75rem"},
        ),
        Style(".question { font-weight: bold; margin-bottom: 0.5rem; }"),
    )


@hx.route("/ask", methods=["POST"])
async def ask(prompt: str = FastAPIForm("")) -> object:
    """Async generator: first event is the question block, then the tokens."""
    GENERATION["active"] = True
    try:
        yield Div(prompt.strip() or "(no question)", class_="question")
        for token in fake_model_answer(prompt):
            if not GENERATION["active"]:
                return  # /clear cancelled mid-stream
            await asyncio.sleep(0.04)
            # RawHTML so each event appends an inline text fragment, not a block.
            yield RawHTML(f" {token}")
    finally:
        GENERATION["active"] = False


@hx.route("/clear", methods=["POST"])
async def clear() -> Component:
    """Stop any in-flight generation; empty body empties the transcript."""
    GENERATION["active"] = False
    return Div()


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
