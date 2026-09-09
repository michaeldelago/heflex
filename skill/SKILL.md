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
from heflex import Heflex
from heflex.component import Div, Button

hx = Heflex(FastAPI(title="My App", debug=True))

@hx.route("/")          # GET by default; pass methods=["POST"] for others
async def home() -> Component:
    return Div("hello")

app = hx.app            # expose the underlying FastAPI app for uvicorn
```

**Tip: make scripts directly runnable with a uv shebang.** The examples (`./example/counter.py`) start with:

```python
#!/usr/bin/env -S uv run --script
#
# /// script
# requires-python = ">=3.14"
# dependencies = ["heflex", "uvicorn"]
#
# [tool.uv.sources]
# heflex = { path = "../", editable = true }
# ///
```

This PEP 723 inline metadata lets `./example/counter.py` run itself — `uv` resolves and installs the deps on the fly (the `[tool.uv.sources]` entry points at this repo for a local editable copy). Copy the block into new app files to make them self-contained; drop the `sources` section when installing heflex from PyPI instead.

## Core API

### `Heflex(app=FastAPI(), page_layout=DefaultPageLayout)`

Both parameters have defaults: `app` auto-creates a fresh `FastAPI()` when omitted (`hx = Heflex()` works), and `page_layout` is `DefaultPageLayout`.

- `.route(path, methods=["GET"], **kwargs)` — decorator. Accepts sync or async handlers.
- Handler return types: a single `Component`, an iterable of `Components` (rendered and concatenated; empty is valid → empty fragment), or a Starlette/FastAPI `Response` instance (passed through as-is, e.g. `RedirectResponse`). Anything else raises `ValueError` server-side — heflex never silently JSON-encodes your return value.
- **Sync generator handlers are rejected** (`def ...: yield`) with `TypeError` at decoration time (FastAPI would misclassify them as JSONL streams). **Async generators are the SSE path**: `async def h(): yield Component(...)` streams `text/event-stream`; each yielded `Component`/`str`/`RawHTML` is one unnamed event (swapped per hx-target/hx-swap), and `SSEEvent(event="done")` yields a named event for `hx-sse:close`/DOM dispatch. The default layout already loads htmx's `hx-sse` extension; persistent connections use `**{"hx-sse:connect": "/url"}` on an element (colon can't be typed as a kwarg).
- **Request params are special-cased**: if the handler signature does not include a `request: Request` parameter, heflex injects one internally for HTMX detection but strips it from the call to your function. You can also declare `request: Request` yourself and use it normally (cookies, state, etc.).
- **Form data**: use FastAPI's own param machinery — `Annotated[list[str], FastAPIForm()]`, plain scalars, etc. See `example/sortable.py`.

### Components (`heflex.component`)

```python
from heflex.component import Div, Button, H1, Table, Tr, Td, Span, Form, Input, Script, Style, RawHTML

Div(
    H1("Welcome"),
    Input(type="text", placeholder="Enter name"),
    Button("Submit", hx_post="/submit", hx_target="#result"),
    class_="card",
)
```

`Component("tag", *children, **attrs)` works for any tag. All [MDN HTML element tags](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements) are also available as factory functions:

**Root & structure:** `Html`, `Head`, `Body`, `Title`, `Meta`
**Sectioning:** `Main`, `Header`, `Footer`, `Nav`, `Aside`, `Article`, `Section`, `H1`–`H6`, `Hgroup`, `Details`, `Summary`
**Text:** `P`, `Blockquote`, `Pre`, `Code`, `Br`, `Hr`, `Div`, `Span`, `Em`, `Strong`, `Small`, `Mark`, `Abbr`, `Cite`, `Q`, `Dfn`, `Time`, `Data`, `Wbr`
**Inline:** `A`, `Img`, `I`, `B`, `U`, `S`, `Sub`, `Sup`, `Kbd`, `Var`, `Samp`, `Del`, `Ins`, `Rp`, `Rt`, `Ruby`, `Bdi`, `Bdo`
**Media:** `Picture`, `Source`, `Video`, `Audio`, `Canvas`, `Map`, `Area`, `Figcaption`, `Figure`
**Embedded:** `Iframe`, `Embed`, `Object`, `Param`, `Svg`, `Math`
**Forms:** `Form`, `Fieldset`, `Legend`, `Label`, `Input`, `Button`, `Select`, `Option`, `Optgroup`, `Textarea`, `Datalist`, `Output`, `Progress`, `Meter`
**Tables:** `Table`, `Thead`, `Tbody`, `Tfoot`, `Tr`, `Th`, `Td`, `Caption`, `Col`, `Colgroup`
**Interactive:** `Menu`, `Li`, `Ul`, `Ol`, `Dialog`
**Web components:** `Slot`, `Template`

Deprecated/obsolete tags (`Acronym`, `Applet`, `Basefont`, `Bgsound`, `Dir`, `Font`, `Frame`, `Frameset`, `Noframes`, `Isindex`, `Listing`, `Marquee`, `Multicol`, `Nextid`, `Strike`, `TT`, `Xmp`) are available from `heflex.component.deprecated` and emit `DeprecationWarning` at construction time.

`Script(content, **kwargs)` and `Style(css_text, **kwargs)` take content as the first positional arg (text is emitted raw, not escaped). `RawHTML(...)` interpolates verbatim.

- Children can be strings, nested Components, or `RawHTML`. String children are HTML-escaped by default; wrap pre-built HTML in `RawHTML(...)` to interpolate it verbatim. `Script`/`Style` content is always emitted raw (browsers parse those tags as raw text).
- `Input`, and tags `img/br/hr/meta`, render self-closing: `Input(name="q", type="text")`.

### Attribute rules (gotchas!)

- **snake_case kwargs become hyphenated HTML attrs**: `hx_post="/x"` → `hx-post="/x"`, `class_` → ... see below. So HTMX attrs are written as kwargs `hx_get`, `hx_post`, `hx_target`, `hx_swap`, `hx_trigger`.
- **Trailing underscore** on a kwarg name is stripped: `class_="foo"` → `class="foo"`. (Needed for `class`.) There is no `for_` special-casing beyond this general rule, so write `for="id"` via `for_=`.
- **Literal underscore escape**: to emit a real `_` at the end of an attribute name, double it: `data_foo__=...` renders `data-foo_=...`. All other underscores still become hyphens.
- **Booleans** render as `attr="true"` or are omitted when `False` (HTMX v4 style). Never pass string `"true"`.
- **`style` is a dict**, not a CSS string: `style={"margin": "1rem", "color": "red"}`. Keys/values are stripped and joined with `; `. Keys are emitted verbatim, so pseudo-class keys (e.g. `"background-color:hover"`) do reach the browser but are ignored as invalid inside `style=""` — use a real `<Style>` block with ids/classes for selectors.

### Page layout

Signature: `Callable[[str, *Component], Component]` — receives `(title, *children)` and must return a `Component`. The title comes from `FastAPI`'s `title`. Heflex prepends `<!DOCTYPE html>` to the rendered layout (layouts start at `<html>`; HTMX fragments get no doctype). Default loads HTMX v4 from unpkg CDN (`htmx.org@4.0.0`) into `<head>` and wraps in a styled `<body>`.

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
