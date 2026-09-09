import pytest
from fastapi import FastAPI
from starlette.testclient import TestClient

from heflex.component import Button, Component, Div
from heflex import Heflex, SSEEvent


def make_sse_app() -> Heflex:
    hx = Heflex(FastAPI(title="SSE"))

    @hx.route("/", methods=["GET"])
    async def home():
        return [
            Button(
                "Generate",
                hx_get="/gen",
                hx_target="#output",
                hx_swap="beforeend",
            ),
            Div(id="output"),
        ]

    @hx.route("/gen", methods=["GET"])
    async def gen():
        # multiline text, a component, and a named close event
        yield "a\nb"
        yield Component("p", "chunk")
        yield SSEEvent(event="done", data="")

    @hx.route("/returned-agen", methods=["GET"])
    async def returned_agen():
        async def stream():
            yield Div("hi")

        return stream()

    return hx


def test_default_layout_includes_hx_sse_extension():
    c = TestClient(make_sse_app().app)
    html = c.get("/").text
    assert "htmx.min.js" in html
    assert "ext/hx-sse.min.js" in html
    assert html.startswith("<!DOCTYPE html>")


def test_async_generator_handler_streams_sse():
    c = TestClient(make_sse_app().app)
    with c.stream("GET", "/gen") as r:
        assert r.status_code == 200
        assert r.headers["content-type"].startswith("text/event-stream")
        body = "".join(r.iter_text())

    # newline-safe framing of the text payload
    assert "data: a\ndata: b\n\n" in body
    # components render to HTML inside unnamed events
    assert 'data: <p>chunk</p>\n\n' in body
    # named event for hx-sse:close / DOM dispatch
    assert "event: done\ndata:\n\n" in body


def test_returned_async_generator_object_streams_sse():
    c = TestClient(make_sse_app().app)
    with c.stream("GET", "/returned-agen") as r:
        assert r.headers["content-type"].startswith("text/event-stream")
        body = "".join(r.iter_text())
    assert 'data: <div>hi</div>\n\n' in body


def test_yielding_non_component_raises_type_error():
    from heflex.sse import frame_item

    with pytest.raises(TypeError, match=r"must yield Component"):
        frame_item(42)


def test_sse_event_framing_rules():
    out = SSEEvent(data="x", event="tick", id="e1", retry=2000).frame()
    assert out == "event: tick\nid: e1\nretry: 2000\ndata: x\n\n"


def test_sse_event_rejects_invalid_names():
    with pytest.raises(ValueError, match=r"must not contain"):
        SSEEvent(event="bad name").frame()
