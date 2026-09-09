#!/usr/bin/env -S uv run --script
#
# "Edit in Place" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/edit-in-place
#
# View mode shows the current values plus an Edit button that fetches the edit
# form (hx-get /users/<id>/edit); hx-target="this" + hx-swap="outerHTML" on the
# card replace it with the response. The edit form submits as a PUT (hx-put) —
# Save updates and the server responds with the view-mode HTML; Cancel simply
# re-fetches the view without saving. Endpoints follow REST conventions:
# GET /users/<id> (view), GET /users/<id>/edit (form), PUT /users/<id> (update).
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
from heflex.component import Button, Component, Div, Form, H1, Input, P, Strong, Style
from heflex import Heflex


class User:
    def __init__(self, id_: int, name: str, email: str):
        self.id_, self.name, self.email = id_, name, email


USERS: dict[int, User] = {
    1: User(1, "Joe Smith", "joe@smith.org"),
    2: User(2, "Amy Jones", "amy@example.com"),
}


def view_card(u: User) -> Component:
    """View mode. The card targets itself so any inner request can replace it."""
    return Div(
        P(Strong("Name:"), u.name),
        P(Strong("Email:"), u.email),
        Button(
            "Edit",
            type="button",
            hx_get=f"/users/{u.id_}/edit",
            hx_target=f"#card-{u.id_}",
            hx_swap="outerHTML",
        ),
        id=f"card-{u.id_}",
        class_="card",
    )


def edit_card(u: User) -> Component:
    """Edit mode: form pre-filled with the current values."""
    return Div(
        Form(
            Input(type="text", name="name", value=u.name),
            Input(type="email", name="email", value=u.email),
            Button("Save", type="submit"),
            Button(
                "Cancel",
                type="button",
                hx_get=f"/users/{u.id_}",
                hx_target=f"#card-{u.id_}",
                hx_swap="outerHTML",
            ),
            hx_put=f"/users/{u.id_}",
            hx_target=f"#card-{u.id_}",
            hx_swap="outerHTML",
        ),
        id=f"card-{u.id_}",
        class_="card",
    )


hx = Heflex(FastAPI(debug=True, title="Edit in Place"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Users"),
        *(view_card(u) for u in USERS.values()),
        Style(
            ".card { border: 1px solid #ccc; padding: 0.75rem; margin-bottom: 0.75rem; max-width: 24rem; background: white; }"
        ),
    )


@hx.route("/users/{user_id}", methods=["GET"])
async def get_user(user_id: int) -> Component:
    """The view-mode card (used by Cancel)."""
    return view_card(USERS[user_id])


@hx.route("/users/{user_id}/edit", methods=["GET"])
async def get_user_edit(user_id: int) -> Component:
    """The pre-filled edit form."""
    return edit_card(USERS[user_id])


@hx.route("/users/{user_id}", methods=["PUT"])
async def update_user(
    user_id: int, name: str = FastAPIForm(""), email: str = FastAPIForm("")
) -> Component:
    """Save: update the resource and respond with the view-mode HTML."""
    u = USERS[user_id]
    if name.strip() and email.strip():
        u.name, u.email = name.strip(), email.strip()
    return view_card(u)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
