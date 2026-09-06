#!/usr/bin/env -S uv run --script
#
# "Reset on Submit" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/reset-on-submit
#
# The form wraps its inputs and uses hx-on to reset itself after each
# successful request: hx-post submits to /chat, hx-target points at the
# #messages container, hx-swap="beforeend" appends each new message to the
# bottom, and hx-on:htmx:after:request calls this.reset() to clear the form.
# (For standalone inputs without a <form>, select the element in the handler
# and clear .value directly — reset() only exists on form elements.)
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uvicorn
from fastapi import FastAPI, Form as FastAPIForm
from heflex import Button, Component, Div, Form, Heflex, Input, Style


def bubble(text: str, sender: str) -> Component:
    align = "right" if sender == "you" else "left"
    return Div(
        text,
        style={
            "max-width": "70%",
            "text-align": align,
            "margin-left": "auto" if sender == "you" else "0",
            "margin-right": "0" if sender == "you" else "auto",
            "background": "#e0e0ff" if sender == "you" else "#eee",
            "padding": "0.5rem",
            "border-radius": "8px",
            "margin-bottom": "0.4rem",
        },
    )


hx = Heflex(FastAPI(debug=True, title="Reset on Submit"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        Component("h1", "Chat"),
        Div(
            bubble("Hi! How can I help?", "bot"),
            id="messages",
            style={"max-width": "70%", "margin-left": "auto", "border": "1px solid #ccc", "padding": "0.75rem"},
        ),
        Form(
            Input(type="text", name="message", placeholder="Say something…"),
            Button("Send", type="submit"),
            hx_post="/chat",
            hx_target="#messages",
            hx_swap="beforeend",
            **{"hx-on:htmx:after:request": "this.reset()"},
        ),
    )


@hx.route("/chat", methods=["POST"])
async def chat(message: str = FastAPIForm("")) -> list[Component]:
    """The user's message plus a canned reply, appended to #messages."""
    message = message.strip() or "(empty)"
    return [bubble(message, "you"), bubble(f"Echo: {message}", "bot")]


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
