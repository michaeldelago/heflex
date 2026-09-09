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

heflex is not yet published to PyPI; install it from this repository (path or git):

```bash
uv add /path/to/heflex
# or: uv add "heflex @ git+https://<your-repo-url>"
```

Once it's on PyPI, `uv add heflex` will work as-is.

Requires Python 3.14+. Dependencies: `fastapi`, `python-multipart`. The files in `example/` are self-contained via PEP 723 inline metadata — just run them with `uv run example/counter.py`.

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
    return await home()

app = hx.app
```

Run with (`uvicorn` is a dev dependency, not part of heflex):

```bash
uv add uvicorn
uv run uvicorn main:app --reload
```

## API

### Components

A `Component` represents an HTML element with a tag, children, and attributes:

```python
from heflex.component import Div, Button, Input, Form, H1, Table, Tr, Td, Span
from heflex import Script, Style, RawHTML

Div(
    H1("Welcome"),
    Input(type="text", placeholder="Enter name"),
    Button("Submit", hx_post="/submit", hx_target="#result"),
    class_="card",
    style={"padding": "1rem", "border-radius": "8px"},
)
```

Snake_case kwargs are converted to hyphenated HTML attributes:
- `hx_post="/api"` → `hx-post="/api"`
- `hx_boost=True` → `hx-boost="true"`
- `class_="foo bar"` → `class="foo bar"` (trailing `_` is stripped; double it — `data_foo__=` — to emit a literal trailing underscore: `data-foo_=`)

Boolean attributes render as `attr="true"` when truthy, and are omitted when false.
The `style` attribute accepts a dict and joins key-value pairs as CSS.

Attribute values and string children are HTML-escaped. Wrap pre-built HTML in
`RawHTML(...)` to interpolate it verbatim; `Script`/`Style` content is always
emitted raw (browsers parse those tags as raw text).

#### Factory functions

All [MDN HTML element tags](https://developer.mozilla.org/en-US/docs/Web/HTML/Reference/Elements) are available as factory functions, imported from `heflex.component`. Each function returns a `Component` with the corresponding tag.

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

The following are deprecated/obsolete and emit a `DeprecationWarning` at construction time:
`Acronym`, `Applet`, `Basefont`, `Bgsound`, `Dir`, `Font`, `Frame`, `Frameset`, `Noframes`, `Isindex`, `Listing`, `Marquee`, `Multicol`, `Nextid`, `Strike`, `TT`, `Xmp`.

Built-in helpers: `Script`, `Style`, `RawHTML`, `Component`.

### Route Decorator

`@hx.route()` wraps a FastAPI route handler:

```python
@hx.route("/path", methods=["GET", "POST"])
async def handler(some_arg: str) -> Component:
    return Div(f"Got: {some_arg}")
```

The handler returns a `Component`, an iterable of `Components`, or passes through a `Response` (e.g. `RedirectResponse`). **Async generator** handlers are also first-class: they stream `text/event-stream` (SSE) — see [Server-Sent Events](#server-sent-events-sse). Sync generator handlers are rejected at decoration time (FastAPI would misclassify them as JSONL streams). For HTMX requests (`HX-Request: true`) heflex returns the rendered HTML fragment. For normal requests it wraps the output in a page layout. If the handler does not accept a `Request` parameter, heflex adds one automatically.

### Page Layouts

The default layout wraps content in `<html><head><body>` with HTMX v4 and the `hx-sse` extension from CDN (remove the extension script tag if you don't use SSE). heflex prepends `<!DOCTYPE html>` before the rendered layout, so your layout should start at the `<html>` element (and HTMX fragment responses never include a doctype). Override with a custom function:

```python
def my_layout(title: str, *children: Component) -> Component:
    return Component(
        "html",
        Component("head", Component("title", title), Style("body { color: red; }")),
        Component("body", *children),
    )

hx = Heflex(page_layout=my_layout)
```

## Server-Sent Events (SSE)

heflex ships an SSE path built on htmx 4's [`hx-sse` extension](https://four.htmx.org/extensions/hx-sse) (already loaded by the default layout). An async-generator handler streams `text/event-stream`; each yielded item becomes one SSE message:

- `Component`, `str`, or `RawHTML` → unnamed event — htmx swaps it like an HTML response (`hx-target`/`hx-swap` apply)
- `SSEEvent(event="done", ...)` → named event — dispatches a DOM event / matches `hx-sse:close`; supports `id` (replay) and `retry` fields

```python
@hx.route("/greeting", methods=["GET"])
async def greeting():
    for chunk in ["Hello", ", ", "world", "!"]:
        yield chunk  # each chunk appends to hx-target="#output" hx-swap="beforeend"
```

Persistent connections use `hx-sse:connect="/url"` on an element, closed by a named event (`hx-sse:close="done"`). Returning an async generator object from a regular handler is equivalent to being one. See `example/ticker.py`.

## Examples

Every file is self-contained (PEP 723 inline metadata): `uv run example/counter.py`.

- `counter.py` — Counter using HTMX outerMorph swaps
- `sortable.py` — Drag-and-drop sortable list using SortableJS
- `ticker.py` — SSE: streamed text chunks and a persistent `hx-sse:connect` feed

The remaining files are self-contained ports of the [htmx v4 pattern pages](https://four.htmx.org/patterns) (each cites its source URL in a header comment):

| Category | Examples |
| --- | --- |
| Loading | `click_to_load.py`, `infinite_scroll.py`, `lazy_load.py`, `progress_bar.py` |
| Forms | `active_search.py`, `active_validation.py`, `file_upload.py`, `linked_selects.py`, `reset_on_submit.py` |
| Records | `bulk_actions.py`, `delete_in_place.py`, `drag_to_reorder.py`, `edit_in_place.py` |
| Display | `tabs.py`, `dialogs.py` |
| Streaming | `llm_streaming_response.py`, `live_updates.py`, `polling.py` |
| Advanced | `keyboard_shortcuts.py` |

## License

GPL-3.0
