# heflex

A Python framework for building HTMX applications on FastAPI.

Route handlers return component trees that heflex renders as HTML. For HTMX requests it returns fragments; for normal requests it wraps the output in a full page.

## Features

- Component-based HTML rendering (`Div`, `Button`, `Form`, etc.)
- Automatic HTMX request detection — fragments for HTMX, full pages otherwise
- HTMX v4 loaded from CDN by default
- Snake_case kwargs converted to hyphenated HTML attributes (`hx_post` → `hx-post`)
- Supports sync and async route handlers
- Custom page layout function

## Installation

```bash
uv add heflex
```

Requires Python 3.14+. Dependencies: `fastapi`, `python-multipart`.

## Quick Start

```python
from heflex import Heflex, Div, Button, Component

hx = Heflex()
count = 0

@hx.route("/")
async def home():
    global count
    return Div(
        Component("h1", f"Count: {count}"),
        Button("Increment", hx_post="/inc", hx_target="#wrap", hx_swap="outerMorph"),
        id="wrap",
    )

@hx.route("/inc", methods=["POST"])
async def increment():
    global count
    count += 1
    return home()

app = hx.app
```

Run with:

```bash
uvicorn main:app --reload
```

## API

### Components

A `Component` represents an HTML element with a tag, children, and attributes:

```python
from heflex import Div, Button, Input, Form, Script, Style, Component

Div(
    Input(type="text", placeholder="Enter name"),
    Button("Submit", hx_post="/submit", hx_target="#result"),
    class_="card",
    style={"padding": "1rem", "border-radius": "8px"},
)
```

Snake_case kwargs are converted to hyphenated HTML attributes:
- `hx_post="/api"` → `hx-post="/api"`
- `hx_boost=True` → `hx-boost="true"`
- `class_="foo bar"` → `class="foo bar"`

Boolean attributes render as `attr="true"` when truthy, and are omitted when false.
The `style` attribute accepts a dict and joins key-value pairs as CSS.

Built-in helpers: `Div`, `Button`, `Input`, `Form`, `Script`, `Style`.

### Route Decorator

`@hx.route()` wraps a FastAPI route handler:

```python
@hx.route("/path", methods=["GET", "POST"])
async def handler(some_arg: str) -> Component:
    return Div(f"Got: {some_arg}")
```

The handler returns a `Component` or iterable of `Components`. For HTMX requests (`HX-Request: true`) heflex returns the rendered HTML fragment. For normal requests it wraps the output in a page layout. If the handler does not accept a `Request` parameter, heflex adds one automatically.

### Page Layouts

The default layout wraps content in `<html><head><body>` with HTMX v4 from CDN. Override with a custom function:

```python
def my_layout(title: str, *children: Component) -> Component:
    return Component(
        "html",
        Component("head", Component("title", title), Style("body { color: red; }")),
        Component("body", *children),
    )

hx = Heflex(page_layout=my_layout)
```

## Examples

The `example/` directory contains two runnable applications:

- `counter.py` — Counter using HTMX outerMorph swaps
- `sortable.py` — Drag-and-drop sortable list using SortableJS

```bash
cd example
uv run counter.py
uv run sortable.py
```

## License

GPL-3.0
