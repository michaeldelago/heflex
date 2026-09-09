#!/usr/bin/env -S uv run --script
#
# "Lazy Load" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/lazy-load
#
# Placeholders with hx-trigger="load" fire requests as soon as they enter
# the DOM (i.e. immediately, in parallel for multiple placeholders), and
# the server's HTML is swapped into each one when it arrives — so a page
# renders fast even if several sections are slow. Each placeholder reserves
# min-height space to limit layout shift (CLS). Note: never include
# hx-trigger="load" in the *response* of the same endpoint or you get an
# infinite load loop.
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
from heflex.component import Component, Div, H1, H2, H3
from heflex import Heflex


def placeholder(label: str, url: str) -> Div:
    """A self-replacing loading box that fires on load (min-height reserves space)."""
    return Div(
        f"{label} ...",
        hx_get=url,
        hx_trigger="load",
        hx_swap="innerHTML",
        min_height="3rem",
        style={
            "border": "1px dashed #ccc",
            "padding": "0.75rem",
            "margin-bottom": "1rem",
        },
    )


hx = Heflex(FastAPI(debug=True, title="Lazy Load"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    """
    One basic section plus a set of independent sections that all load in
    parallel. Responses below contain no hx-trigger="load", so no loop.
    """
    return Div(
        H1("Dashboard"),
        placeholder("Loading weather", "/weather"),
        Div(
            H2("Parallel sections"),
            placeholder("Loading sales", "/sales"),
            placeholder("Loading analytics", "/analytics"),
            placeholder("Loading notifications", "/notifications"),
        ),
    )


@hx.route("/weather", methods=["GET"])
async def weather() -> Component:
    """Might query a database or call an external API."""
    return Div(
        H3("5-Day Forecast"),
        *map(
            lambda i: Div(f"Weekday {i}: 7{2 - i}° Sunny", style={"padding": "0.1rem"}),
            range(1, 6),
        ),
    )


@hx.route("/sales", methods=["GET"])
async def sales() -> Component:
    return Div("Sales are up 12% week over week.")


@hx.route("/analytics", methods=["GET"])
async def analytics() -> Component:
    return Div("Bounce rate 34%, avg session 2m 40s.")


@hx.route("/notifications", methods=["GET"])
async def notifications() -> Component:
    return Div("No new notifications.")


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
