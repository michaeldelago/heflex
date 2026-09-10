#!/usr/bin/env -S uv run --script
#
# "Tabs" pattern — htmx v4 docs:
# https://four.htmx.org/patterns/tabs
#
# Server-driven tabs (HATEOAS): the server owns which tab is selected, and each
# response carries the full tab strip AND the panel. The container starts empty
# and loads the first tab on load; every tab button targets the container with
# hx-swap="innerMorph" — a morph keeps focus on the activated tab so keyboard
# navigation survives the swap. Only aria-selected/tabindex differ between
# responses (a roving tabindex: one Tab stop on the strip, arrows move within).
# One keydown handler on the tablist implements arrow-key navigation with
# wrap-around plus Home/End.
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
from heflex.component import Button, Component, Div, H1, Style
from heflex import Heflex

TABS: dict[str, str] = {
    "overview": "Overview content… A short description of the project.",
    "install": "Install content… pip install my-project",
    "extensions": "Extensions content… Plugins live here.",
}
DEFAULT_TAB = "overview"

# Single handler on the tab strip: arrows wrap, Home/End jump. Arrow keys move
# focus AND activate (click) so the server gets the request.
ARROW_JS = (
    "var tabs=[...event.currentTarget.querySelectorAll('[role=tab]')];"
    "var i=tabs.indexOf(document.activeElement);"
    "if(event.key==='ArrowRight'){i=(i+1)%tabs.length;}"
    "else if(event.key==='ArrowLeft'){i=(i-1+tabs.length)%tabs.length;}"
    "else if(event.key==='Home'){i=0;}"
    "else if(event.key==='End'){i=tabs.length-1;}"
    "else{return;}"
    "event.preventDefault();tabs[i].focus();tabs[i].click();"
)


def tab_strip(active: str) -> Component:
    buttons = [
        Button(
            name,
            type="button",
            role="tab",
            id=f"tab-{name}",
            aria_controls=f"panel-{name}",
            aria_selected=str(name == active).lower(),
            tabindex=0 if name == active else -1,
            hx_get=f"/tab?name={name}",
            hx_target="#tabs-container",
            hx_swap="innerMorph",
        )
        for name in TABS
    ]
    return Div(*buttons, role="tablist", **{"hx-on:keydown": ARROW_JS})


def render_tab(name: str) -> list[Component]:
    """Tab strip plus panel; swapped together into the container."""
    return [
        tab_strip(name),
        Div(
            TABS[name],
            role="tabpanel",
            id=f"panel-{name}",
            aria_labelledby=f"tab-{name}",
        ),
    ]


hx = Heflex(FastAPI(debug=True, title="Tabs"))


@hx.route("/", methods=["GET"])
async def index() -> Component:
    return Div(
        H1("Server-driven tabs"),
        # Empty container; hx-trigger=load fetches the first tab. It targets
        # itself and :inherited so every fetched strip's buttons target it too.
        Div(
            hx_get=f"/tab?name={DEFAULT_TAB}",
            hx_target="this",
            hx_swap="innerMorph",
            hx_trigger="load",
            id="tabs-container",
        ),
        Style(
            """
            [role=tab] { padding: 0.5rem 1rem; border: none; background: none; cursor: pointer; border-bottom: 2px solid transparent; }
            [role=tab][aria-selected=true] { border-bottom: 2px solid currentColor; font-weight: bold; }
            [role=tabpanel] { padding: 1rem; border: 1px solid #ccc; margin-top: 0.5rem; }
            """
        ),
    )


@hx.route("/tab", methods=["GET"])
async def tab(name: str = Query(DEFAULT_TAB)) -> list[Component]:
    if name not in TABS:
        name = DEFAULT_TAB
    return render_tab(name)


app = hx.app

if __name__ == "__main__":
    uvicorn.run(app, port=8000)
