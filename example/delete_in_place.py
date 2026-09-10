#!/usr/bin/env -S uv run --script
#
# "Delete in Place" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/delete-in-place
#
# Each row's delete button carries: hx-confirm (prompts before the request),
# hx-target="closest tr" (the row containing the button), and
# hx-swap="outerHTML swap:500ms", which delays the row replacement by 500 ms so
# a CSS fade-out can play — during that delay htmx adds the htmx-swapping
# class to the target row, and tr.htmx-swapping td { opacity: 0 } fades it.
# hx-delete sends a DELETE request; the server responds with an empty body and
# 200, so the row is simply removed. (In htmx 4 these attributes could instead
# live once on <tbody> with the :inherited modifier.)
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
from heflex.component import Button, Component, Div, H1, Style, Table, Td, Th, Tr, Tfoot
from heflex import Heflex
from starlette.responses import PlainTextResponse


class User:
    def __init__(self, name: str, email: str, status: str):
        self.name, self.email, self.status = name, email, status


USERS = [
    User("Angie MacDowell", "angie@macdowell.org", "active"),
    User("Ben Carter", "ben@carter.dev", "inactive"),
    User("Cleo Rivera", "cleo@rivera.io", "active"),
]


def row(u: User) -> Component:
    return Tr(
        Td(u.name),
        Td(u.email),
        Td(u.status.capitalize()),
        Td(
            Button(
                "Delete",
                type="button",
                hx_confirm="Are you sure you want to delete this user?",
                hx_target="closest tr",
                hx_swap="outerHTML swap:500ms",
                hx_delete=f"/users/{u.email}",
            ),
        ),
    )


hx = Heflex(FastAPI(debug=True, title="Delete in Place"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Users"),
        Table(
            Tr(*(Th(h) for h in ("Name", "Email", "Status", ""))),
            *(row(u) for u in USERS),
            style={"border-collapse": "collapse", "width": "100%"},
        ),
        Style(
            """
            th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
            tr.htmx-swapping td { opacity: 0; transition: opacity 500ms ease-out; }
            """
        ),
    )


@hx.route("/users/{email}", methods=["DELETE"])
async def delete_user(email: str) -> PlainTextResponse:
    """Empty body + 200: the targeted row is replaced with nothing."""
    global USERS
    USERS = [u for u in USERS if u.email != email]
    return PlainTextResponse("", status_code=200)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
