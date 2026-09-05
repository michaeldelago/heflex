---
name: heflex
description: Build HTMX web applications on FastAPI using the heflex Python library (component trees rendered to HTML). Use when creating or modifying routes, components, or layouts in a project that depends on heflex.
---

# Heflex

Python framework for HTMX apps on FastAPI. Route handlers return **component trees** (Python objects), not HTML strings. heflex renders them: HTMX requests (`HX-Request: true` header) get fragments, normal requests get a full page via the layout function.

Reference material lives in this repo: `README.md` and the runnable apps `example/counter.py` (outerMorph swaps) and `example/sortable.py` (SortableJS drag-and-drop with a custom page layout). Read those before making non-trivial changes.

## Setup

Python 3.14+, deps are `fastapi` and `python-multipart`. Install with `uv add heflex`.

App skeleton:

```python
from fastapi import FastAPI
from heflex import Heflex, Component, Div, Button

hx = Heflex(FastAPI(title="My App", debug=True))

@hx.route("/")          # GET by default; pass methods=["POST"] for others
async def home() -> Component:
    return Div("hello")

app = hx.app            # expose the underlying FastAPI app for uvicorn
```

## Core API

### `Heflex(app=None, page_layout=DefaultPageLayout)`

- `.route(path, methods=["GET"], **kwargs)` — decorator. Accepts sync or async handlers.
- Handler return types: a single `Component`, a list/iterable of `Components` (rendered and concatenated), or any other FastAPI-compatible response (returned as-is, e.g. redirect).
- **Request params are special-cased**: if the handler signature does not include a `request: Request` parameter, heflex injects one internally for HTMX detection but strips it from the call to your function. You can also declare `request: Request` yourself and use it normally (cookies, state, etc.).
- **Form data**: use FastAPI's own param machinery — `Annotated[list[str], FastAPIForm()]`, plain scalars, etc. See `example/sortable.py`.

### Components (`heflex.component`)

```python
Component("h1", "text", children_or_text..., **attributes)   # any tag
Div(*children, **kwargs)     Button(...)  Input(...)  Form(...)
Script(content, **kwargs)    Style(css_text, **kwargs)       # text content is first positional arg
```

- Children can be strings or nested Components. Plain strings are interpolated as-is (no escaping — build values from trusted/own data).
- `Input`, and tags `img/br/hr/meta`, render self-closing: `Input(name="q", type="text")`.

### Attribute rules (gotchas!)

- **snake_case kwargs become hyphenated HTML attrs**: `hx_post="/x"` → `hx-post="/x"`, `class_` → ... see below. So HTMX attrs are written as kwargs `hx_get`, `hx_post`, `hx_target`, `hx_swap`, `hx_trigger`.
- **Trailing underscore** on a kwarg name is stripped: `class_="foo"` → `class="foo"`. (Needed for `class`.) There is no `for_` special-casing beyond this general rule, so write `for="id"` via `for_=`.
- **Booleans** render as `attr="true"` or are omitted when `False` (HTMX v4 style). Never pass string `"true"`.
- **`style` is a dict**, not a CSS string: `style={"margin": "1rem", "color": "red"}`. Keys/values are stripped and joined with `; `. The sortable example abuses this for pseudo-class keys (`"background-color:hover"`), which the renderer supports verbatim but plain browsers will ignore — prefer real `<Style>` blocks for selectors.

### Page layout

Signature: `Callable[[str, *Component], Component]` — receives `(title, *children)` and must return a `Component`. The title comes from `FastAPI`'s `title`. Default loads HTMX v4 from unpkg CDN (`htmx.org@4.0.0`) into `<head>` and wraps in a styled `<body>`.

Custom layout (e.g. to add your own JS/CSS or SortableJS):

```python
def page_layout(title: str, *args: Component) -> Component:
    return Component(
        "html",
        Component("head", Component("title", title),
                  Script("", src="https://unpkg.com/htmx.org@4.0.0/dist/htmx.min.js"),
                  Style(my_css)),
        Component("body", *args),
    )

hx = Heflex(FastAPI(title="App", debug=True), page_layout=page_layout)
```

Keep the HTMX script tag in your custom layout — fragments only work if htmx is on the initial page.

## Patterns

**HTMX round-trip**: interactive element carries `hx_post=<route>`, `hx_target="#<id>"` (or `this`), `hx_swap="outerMorph"` (v4) / `innerHTML`; the handler returns the updated component(s). The returned fragment replaces the target — no need to re-render the page.

**Client-side events**: `Form(*items, hx_post="/items", hx_trigger="end")` on a form fires HTMX when SortableJS emits `end`; hidden `Input(name="item", type="hidden")` inside each row carry the new order back as repeated POST fields.

**Loading feedback**: `Div("Updating...", class_="htmx-indicator")` inside the submitted element shows during requests automatically.

**State**: handlers run in a single process; module-level state (a list, or a `{"value": 0}` dict if you mutate) is the standard example pattern. For real apps use FastAPI state/dependencies.

## Conventions when editing heflex code

- Return components, never hand-built HTML strings, from `@hx.route` handlers.
- POST routes: pass `methods=["POST"]`.
- Any attribute containing a hyphen (all `hx-*`) is written as a snake_case kwarg in Python.
- CSS goes through `style={...}` dicts on elements or `<Style>` blocks in the layout — not via raw strings.
- Test by running with uvicorn: `uv run python -m uvicorn module:app`. For behavior checks, hit a route and verify both (a) plain GET returns the full page and (b) `curl -H 'HX-Request: true'` returns only the fragment.
