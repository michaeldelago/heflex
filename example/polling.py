#!/usr/bin/env -S uv run --script
#
# "Polling" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/polling
#
# hx-trigger="every 2s" polls /cpu; hx-swap="outerMorph" replaces the card with
# the same element carrying fresh data (a morph keeps focus, scroll position
# and CSS transitions intact). A filter after the interval stops network
# traffic while the tab is in the background — the interval still runs, so the
# poll resumes when the user returns. Stopping a poll: return the element
# WITHOUT the trigger attributes; htmx clears the interval when the element
# (or its attributes) leave the DOM, which is how Pause works here. Notes: for
# job-style polling use hx-trigger="load delay:1s" (see progress-bar); each
# poll is a full request, so poll no faster than the data changes — for
# high-frequency updates a persistent connection (live-updates / SSE) costs
# less; htmx queues at most one waiting request per element (hx-sync to tune).
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import random

import uvicorn
from fastapi import FastAPI
from heflex.component import Button, Component, Div, H1, Style
from heflex import Heflex

STATE = {"running": True}


def poll_card() -> Component:
    """The card htmx polls; without the trigger attrs the poll is stopped."""
    attrs: dict[str, object] = {
        "id": "poll-card",
        "hx-swap": "outerMorph",
        "style": {
            "border": "1px solid #ccc",
            "padding": "1rem",
            "margin-bottom": "0.75rem",
        },
    }
    if STATE["running"]:
        attrs["hx-get"] = "/cpu"
        # Filter: no traffic while the tab is hidden; interval keeps running.
        attrs["hx-trigger"] = "every 2s filter document.visibilityState === 'visible'"
    label = (
        f"CPU {random.randint(5, 95)}%" if STATE["running"] else "Job complete (paused)"
    )
    return Div(
        Div(label, style={"font-weight": "bold", "margin-bottom": "0.5rem"}),
        Button(
            "Pause" if STATE["running"] else "Resume",
            type="button",
            hx_post="/toggle",
            hx_target="#poll-card",
            hx_swap="outerHTML",
        ),
        **attrs,
    )


hx = Heflex(FastAPI(debug=True, title="Polling"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Polling"),
        poll_card(),
        Style(
            "#poll-card { border: 1px solid #ccc; padding: 1rem; margin-bottom: 0.75rem; }"
        ),
    )


@hx.route("/cpu", methods=["GET"])
async def cpu() -> Component:
    """Same element, fresh data — the card replaces itself via outerMorph."""
    return poll_card()


@hx.route("/toggle", methods=["POST"])
async def toggle() -> Component:
    """Flip running; the paused card omits hx-get/hx-trigger so the poll stops."""
    STATE["running"] = not STATE["running"]
    return poll_card()


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
