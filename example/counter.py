from fastapi import FastAPI, Request
from heflex import Button, Component, Div, Heflex, Script

count_state = {"value": 0}

hx = Heflex(FastAPI(debug=True, title="Counter"))


@hx.route("/", methods=["GET"])
async def counter_view() -> Component:
    """
    Renders the counter element using HTMX v4 morphing.
    """
    return Div(
        Component(
            "h1",
            f"Count: {count_state['value']}",
            style={"max-width": "70%", "margin-left": "auto", "margin-right": "auto"},
        ),
        Div(
            Button(
                "Increment",
                hx_post="/counter/increment",
                hx_target="#counter-wrapper",
                hx_swap="outerMorph",
                style={
                    "color": "white",
                    "padding-left": "1rem",
                    "padding-right": "1rem",
                    "background-color": "oklch(54.6% 0.245 262.881)",
                    "background-color:hover": "oklch(48.8% 0.243 264.376)",
                    "margin-left": "1rem",
                    "margin-right": "1rem",
                    "border-radius": "4px",
                    "max-width": "40%",
                },
            ),
            Button(
                "Decrement",
                hx_post="/counter/decrement",
                hx_target="#counter-wrapper",
                hx_swap="outerMorph",
                style={
                    "color": "white",
                    "padding-left": "1rem",
                    "padding-right": "1rem",
                    "background-color": "oklch(57.7% 0.245 27.325)",
                    "background-color:hover": "oklch(50.5% 0.213 27.518)",
                    "margin-left": "1rem",
                    "margin-right": "1rem",
                    "border-radius": "4px",
                    "max-width": "40%",
                },
            ),
        ),
        id="counter-wrapper",
        style={
            "padding": "2rem",
            "border-radius": "4px",
            "box-shadow": "0 4px 8 px 0 rgba(0,0,0,0.6)",
            "display": "inline-block",
        },
    )


@hx.route("/counter/increment", methods=["POST"])
async def increment() -> Component:
    count_state["value"] += 1
    return await counter_view()


@hx.route("/counter/decrement", methods=["POST"])
async def increment() -> Component:
    count_state["value"] -= 1
    return await counter_view()


app = hx.app
