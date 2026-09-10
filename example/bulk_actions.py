#!/usr/bin/env -S uv run --script
#
# "Bulk Actions" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/bulk-actions
#
# The table is wrapped in a <form>. Each row has a checkbox (name="selected");
# clicking the whole row toggles it (with an event.target guard so clicking
# the checkbox itself doesn't double-toggle). An action bar appears only when
# something is checked (pure CSS :has()). Each action button POSTs to its own
# endpoint — only checked values are submitted — and every response replaces
# the entire form (hx-swap="outerHTML") with a re-rendered table plus a flash
# message. A header checkbox toggles select-all.
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
from heflex.component import (
    Button,
    Component,
    Div,
    Form,
    H1,
    Input,
    P,
    Style,
    Table,
    Td,
    Th,
    Tr,
    Thead,
)
from heflex import Heflex


class User:
    def __init__(self, name: str, email: str, status: str):
        self.name, self.email, self.status = name, email, status


USERS = [
    User("Joe Smith", "joe@smith.org", "active"),
    User("Amy Jones", "amy@example.com", "inactive"),
    User("Max Power", "max@power.io", "active"),
]

# Single quotes so the attribute value survives heflex's HTML escaping intact:
ROW_JS = 'if (event.target.tagName !== "INPUT") this.querySelector("input").click();'


hx = Heflex(FastAPI(debug=True, title="Bulk Actions"))


def full_table(flash: str | None) -> Component:
    rows = [
        Tr(
            Td(Input(type="checkbox", **{"name": "selected", "value": u.email})),
            Td(u.name),
            Td(u.email),
            Td(u.status.capitalize()),
            onclick=ROW_JS,
        )
        for u in USERS
    ]
    action_bar = Div(
        Button(
            "Activate",
            type="button",
            hx_post="/bulk/activate",
            hx_target="#bulk",
            hx_swap="outerHTML",
        ),
        Button(
            "Deactivate",
            type="button",
            hx_post="/bulk/deactivate",
            hx_target="#bulk",
            hx_swap="outerHTML",
        ),
        Button(
            "Delete",
            type="button",
            hx_post="/bulk/delete",
            hx_target="#bulk",
            hx_swap="outerHTML",
        ),
        class_="action-bar",
    )
    return Form(
        *([P(flash, class_="flash")] if flash else []),
        action_bar,
        Table(
            Thead(
                Tr(
                    Td(Input(
                        type="checkbox",
                        id="select-all",
                        onclick='this.closest("form").querySelectorAll("input[name=selected]").forEach(cb => cb.checked = this.checked)',
                    )),
                    Th("Name"),
                    Th("Email"),
                    Th("Status"),
                ),
            ),
            *rows,
        ),
        id="bulk",
    )


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Users"),
        full_table(None),
        Style(
            """
            .action-bar { display: none; gap: 0.5rem; margin-bottom: 0.75rem; }
            form:has(input[name="selected"]:checked) .action-bar { display: flex; }
            tr:has(input:checked) { background: oklch(93% 0.03 264); }
            table { border-collapse: collapse; width: 100%; cursor: pointer; }
            th, td { border: 1px solid #ccc; padding: 0.5rem; text-align: left; }
            .flash { color: green; font-style: italic; margin: 0.25rem 0; }
            """
        ),
    )


@hx.route("/bulk/activate", methods=["POST"])
async def bulk_activate(selected: list[str] = FastAPIForm([])) -> Component:
    count = 0
    for email in selected:
        for u in USERS:
            if u.email == email and u.status != "active":
                u.status = "active"
                count += 1
    return full_table(f"Activated {count} user")


@hx.route("/bulk/deactivate", methods=["POST"])
async def bulk_deactivate(selected: list[str] = FastAPIForm([])) -> Component:
    count = 0
    for email in selected:
        for u in USERS:
            if u.email == email and u.status != "inactive":
                u.status = "inactive"
                count += 1
    return full_table(f"Deactivated {count} user")


@hx.route("/bulk/delete", methods=["POST"])
async def bulk_delete(selected: list[str] = FastAPIForm([])) -> Component:
    deleted = {u.email for u in USERS if u.email in selected}
    remaining = [u for u in USERS if u.email not in deleted]
    USERS[:] = remaining
    return full_table(f"Deleted {len(deleted)} user")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
