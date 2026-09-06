#!/usr/bin/env -S uv run --script
#
# "Active Validation" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/active-validation
#
# The input validates on each keystroke (debounced): hx-trigger fires on
# "input changed delay:300ms", and hx-target="next span" puts the response
# into the next sibling <span>. The server responds with a validation
# message, or an empty element when the value is valid.
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

TAKEN_USERNAMES = {"admin", "root", "venus"}


hx = Heflex(FastAPI(debug=True, title="Active Validation"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        Component("h1", "Sign Up"),
        Component(
            "label",
            "Choose a username: ",
            Input(
                type="text",
                name="username",
                hx_post="/check-username",
                hx_trigger="input changed delay:300ms",
                hx_target="next span",
            ),
        ),
        # The "next span" target that receives validation messages.
        Component("span"),
        Style(".error { color: oklch(57.7% 0.245 27.325); } .ok { color: green; }"),
    )


@hx.route("/check-username", methods=["POST"])
async def check_username(username: str = Query("")) -> Component:
    """Validation message, or an empty span when the value is valid."""
    username = username.strip()
    if not username:
        return Component("span")
    if len(username) < 3:
        return Component("span", "Too short (minimum 3 characters).", class_="error")
    if username.lower() in TAKEN_USERNAMES:
        return Component("span", f"\"{username}\" is taken.", class_="error")
    return Component("span", "Looks good!", class_="ok")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
