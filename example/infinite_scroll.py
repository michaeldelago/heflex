#!/usr/bin/env -S uv run --script
#
# "Infinite Scroll" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/infinite-scroll
#
# A "Loading more..." placeholder row sits at the end of the table with
# hx-trigger="revealed", so it fetches the next page as soon as it scrolls
# into view. The server responds with new rows plus a fresh placeholder
# pointing one page further — hx-swap="outerHTML" replaces the old
# placeholder, creating a self-extending chain with no client-side state.
# (Use hx-trigger="intersect once" instead when the container itself has
# overflow-y: scroll.)
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
from heflex.component import Component, Div, H1, Style, Table, Td, Th, Tr
from heflex import Heflex

PAGE_SIZE = 3
TOTAL_CONTACTS = 15


def contact_rows(start: int, end: int) -> list[Component]:
    return [
        Tr(Td(f"Agent #{i}"), Td(f"agent{i}@smith.org"))
        for i in range(start, end)
    ]


def loading_row(page: int) -> Component:
    """Self-replacing placeholder row that triggers the next fetch."""
    return Tr(
        Td(
            Div("Loading more...", hx_get=f"/contacts?page={page}", hx_trigger="revealed", hx_swap="outerHTML"),
            style={"color": "#888"},
            **{"colspan": 2},
        ),
    )


def render_table(rows: list[Component], tail_page: int | None) -> Component:
    """Full table for the first page; fragment rows otherwise."""
    all_rows = rows + ([loading_row(tail_page)] if tail_page is not None else [])
    return Table(
        Th("Name"),
        Th("Email"),
        *all_rows,
        style={"border-collapse": "collapse"},
        id="contacts-table",
    )


hx = Heflex(FastAPI(debug=True, title="Infinite Scroll"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    """Initial page: first rows plus the revealed placeholder for page 2."""
    return Div(
        H1("Contacts"),
        render_table(contact_rows(0, PAGE_SIZE), tail_page=2),
        Style("#contacts-table td, #contacts-table th { border: 1px solid #ccc; padding: 0.4rem; }"),
    )


@hx.route("/contacts", methods=["GET"])
async def contacts_page(page: int = Query(1)) -> list[Component]:
    """Next rows plus a fresh placeholder pointing one page further."""
    start = (page - 1) * PAGE_SIZE
    rows = contact_rows(start, start + PAGE_SIZE)
    if start + PAGE_SIZE < TOTAL_CONTACTS:
        rows.append(loading_row(page + 1))
    return rows


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
