import pytest
from fastapi import FastAPI, Query, Request
from fastapi.responses import RedirectResponse
from starlette.testclient import TestClient

from heflex import Button, Component, Div, Heflex


def make_app():
    hx = Heflex(FastAPI(title="Test App"))

    @hx.route("/")
    async def home() -> Component:
        return Div("hello home", id="wrap")

    @hx.route("/sync")
    def sync_view() -> Component:
        return Div("sync view")

    @hx.route("/multi")
    async def multi() -> list[Component]:
        return [Div("one", id="a"), Div("two", id="b")]

    @hx.route("/with-request")
    async def with_request(request: Request) -> Component:
        return Div(f"saw-header:{request.headers.get('x-test', 'none')}")

    return hx


client = TestClient(make_app().app)


def test_full_page_for_normal_request():
    r = client.get("/")
    assert r.status_code == 200
    body = r.text
    assert body.startswith("<!DOCTYPE html>")
    assert "<html" in body and "</html>" in body
    assert "<title>Test App</title>" in body
    assert 'id="wrap"' in body
    # HTMX script tag is included by the default layout
    assert "htmx" in body


def test_fragment_for_htmx_request():
    r = client.get("/", headers={"HX-Request": "true"})
    assert r.status_code == 200
    body = r.text
    assert "<html" not in body and "<body" not in body
    assert 'id="wrap"' in body


def test_sync_handler():
    r = client.get("/sync")
    assert r.status_code == 200
    assert "sync view" in r.text


def test_iterable_of_components_concatenated():
    r = client.get("/multi", headers={"HX-Request": "true"})
    body = r.text
    assert 'id="a"' in body and 'id="b"' in body
    assert "<html" not in body


def test_handler_with_explicit_request_param():
    r = client.get("/with-request", headers={"X-Test": "abc"})
    assert "saw-header:abc" in r.text
    # HTMX detection must still work when request is declared by the handler
    r2 = client.get("/with-request", headers={"HX-Request": "true"})
    assert "<html" not in r2.text


def test_button_component_in_route():
    hx = Heflex(FastAPI(title="B"))

    @hx.route("/")
    async def home() -> Component:
        return Div(Button("go", hx_post="/x"), id="wrap")

    c = TestClient(hx.app)
    assert '<button hx-post="/x">go</button>' in c.get("/").text


def test_query_default_param_resolves():
    # Regression: decorating a handler with a defaulted Query param used to
    # raise ValueError at decoration time (un-defaulted request appended after).
    hx = Heflex(FastAPI(title="T"))

    @hx.route("/q")
    async def with_query(word: str = Query(...)) -> Div:
        return Div(f"word={word}")

    c = TestClient(hx.app, raise_server_exceptions=False)
    r = c.get("/q", params={"word": "hi"}, headers={"HX-Request": "true"})
    assert r.status_code == 200 and "word=hi" in r.text
    # Missing required query param -> FastAPI validation error, not a crash.
    r = c.get("/q")
    assert r.status_code == 422


def test_explicit_request_with_defaulted_param():
    hx = Heflex(FastAPI(title="T"))

    @hx.route("/rq")
    async def rq(request: Request, word: str = Query("d")) -> Div:
        # The wrapper must still inject the real Request instance.
        assert request is not None and request.url.path == "/rq"
        return Div(f"word={word}")

    c = TestClient(hx.app, raise_server_exceptions=False)
    r = c.get("/rq", headers={"HX-Request": "true"})
    assert r.status_code == 200 and "word=d" in r.text
    # Normal request renders through the full-page layout.
    r = c.get("/rq")
    assert "<!DOCTYPE html>" in r.text and "word=d" in r.text


def make_edge_app():
    hx = Heflex(FastAPI(title="Edge"))

    @hx.route("/empty")
    async def empty() -> list[Component]:
        return []

    @hx.route("/badstr")
    async def badstr():
        return "plain string"

    @hx.route("/redirect")
    async def redirect():
        return RedirectResponse("/")

    return hx


def test_empty_list_renders_empty_fragment():
    c = TestClient(make_edge_app().app)
    r = c.get("/empty", headers={"HX-Request": "true"})
    assert r.status_code == 200 and r.text == ""
    # full page is still a valid page with an empty body
    full = c.get("/empty")
    assert full.text.startswith("<!DOCTYPE html>") and "<body" in full.text


def test_plain_string_return_raises_clear_error():
    c = TestClient(make_edge_app().app)
    with pytest.raises(ValueError, match=r"must return a Component"):
        c.get("/badstr")


def test_response_passes_through_untouched():
    c = TestClient(make_edge_app().app, follow_redirects=False)
    r = c.get("/redirect")
    assert r.status_code == 307 and r.headers["location"] == "/"


def test_sync_generator_handler_rejected_at_registration():
    # FastAPI's JSONL-stream detection would misclassify the wrapped handler;
    # heflex refuses generator routes up front instead.
    hx = Heflex(FastAPI(title="T"))

    def gen():
        yield Div("x")

    with pytest.raises(TypeError, match=r"must not be a sync generator"):
        hx.route("/gen")(gen)


def test_async_generator_handler_is_allowed_as_sse():
    # Async generators are the first-class SSE path (see tests/test_sse.py);
    # decoration must succeed.
    hx = Heflex(FastAPI(title="T"))

    async def agen():
        yield Div("x")

    assert hx.route("/agen")(agen) is not None
