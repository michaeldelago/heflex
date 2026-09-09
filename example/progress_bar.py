#!/usr/bin/env -S uv run --script
#
# "Progress Bar" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/progress-bar
#
# A button starts a job; the server responds with a container that polls
# for progress (hx-trigger="every 400ms") and swaps it in place with
# hx-swap="outerMorph", so CSS transitions on transform animate smoothly
# between polls. Each poll returns updated progress. When done, the server
# omits hx-trigger, so the morph tears down the polling interval and it
# stops. The bar animates transform: scaleX() (GPU-composited) rather than
# width to avoid layout thrashing.
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///

import uuid

import uvicorn
from fastapi import FastAPI, Query
from heflex.component import Button, Component, Div, H1, Style
from heflex import Heflex

STEP = 0.15
jobs: dict[str, float] = {}


def progress_container(job_id: str, p: float) -> Div:
    """The self-polling bar element (outerMorph morphs it in place each tick)."""
    return Div(
        Div(
            style={
                "height": "24px",
                "background": "oklch(54.6% 0.245 262.881)",
                "width": "100%",
                "transform": f"scaleX({p:.2f})",
            },
            class_="bar",
        ),
        id="progress-container",
        hx_get=f"/progress?job={job_id}",
        hx_trigger="every 400ms",
        hx_swap="outerMorph",
    )


def bar(job_id: str) -> Component:
    p = min(jobs[job_id], 1.0)
    if p >= 1.0:
        # No hx-trigger in this markup → the morph stops the polling.
        return Div("Done", id="progress-container")
    jobs[job_id] = p + STEP
    return progress_container(job_id, p)


hx = Heflex(FastAPI(debug=True, title="Progress Bar"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Background Job"),
        Button(
            "Start Job",
            hx_post="/job",
            hx_target="#result",
            hx_swap="innerHTML",
            style={"background-color": "oklch(54.6% 0.245 262.881)", "color": "white", "border-radius": "4px"},
        ),
        Div(id="result", min_height="3rem"),
        Style(".bar { width: 100%; transform-origin: left; transition: transform 400ms ease-in-out; }"),
    )


@hx.route("/job", methods=["POST"])
async def start_job() -> Component:
    """Start a job and respond with the polling container."""
    job_id = str(uuid.uuid4())
    jobs[job_id] = 0.0
    return progress_container(job_id, 0.0)


@hx.route("/progress", methods=["GET"])
async def get_progress(job: str = Query("")) -> Component:
    if job not in jobs:
        return Div("Unknown job")
    return bar(job)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
