from heflex import (
    Button,
    Component,
    Div,
    Form,
    Input,
    RawHTML,
    Script,
    Style,
)


def test_basic_tag_and_text_child():
    assert Div("hello").render() == "<div>hello</div>"


def test_nested_components():
    assert (
        Div(Button("go")).render() == "<div><button>go</button></div>"
    )


def test_multiple_children():
    assert Component("p", "a", "b").render() == "<p>ab</p>"


def test_snake_case_attributes_become_hyphenated():
    assert (
        Button("x", hx_get="/path").render()
        == '<button hx-get="/path">x</button>'
    )
    out = Div("x", hx_post="/items", hx_target="#wrap", hx_swap="outerMorph")
    html = out.render()
    assert 'hx-post="/items"' in html
    assert 'hx-target="#wrap"' in html
    assert 'hx-swap="outerMorph"' in html


def test_trailing_underscore_stripped():
    assert (
        Div("x", class_="foo bar").render() == '<div class="foo bar">x</div>'
    )


def test_doubled_trailing_underscore_escapes_literal_underscore():
    # data_foo__ -> data-foo_ (escaped literal underscore)
    assert Div("x", **{"data_foo__": "bar"}).render() == '<div data-foo_="bar">x</div>'


def test_bool_true_renders_true():
    assert Button("x", disabled=True).render() == '<button disabled="true">x</button>'


def test_bool_false_omitted_without_stray_whitespace():
    out = Div("x", disabled=False, id="y").render()
    assert out == '<div id="y">x</div>'
    assert "  " not in out


def test_style_dict_joined_as_css():
    out = Component("div", "a", style={"padding": "4rem", "color": "red"}).render()
    assert out == '<div style="padding: 4rem; color: red">a</div>'


def test_attribute_values_escaped():
    out = Div("x", data_q='a"b<c>').render()
    assert out == '<div data-q="a&quot;b&lt;c&gt;">x</div>'


def test_style_value_escaped_in_attribute():
    out = Component("div", "a", style={"x": 'y"z'}).render()
    assert out == '<div style="x: y&quot;z">a</div>'


def test_text_children_escaped_by_default():
    out = Div('<img src=x onerror=alert(1)>').render()
    assert "<img" not in out
    assert "&lt;img src=x onerror=alert(1)&gt;" in out


def test_script_and_style_content_stays_raw():
    js = "for (var i = 0; i < 3; i++) {}"
    css = "@media (max-width: 600px) { a { color: red } }"
    assert Component("div", Script(js)).render() == f"<div><script>{js}</script></div>"
    assert Style(css).render() == f"<style>{css}</style>"


def test_raw_html_interpolated_verbatim():
    assert Div(RawHTML("<b>bold</b>")).render() == "<div><b>bold</b></div>"


def test_self_closing_tags():
    assert Input(name="q", type="text").render() == '<input name="q" type="text" />'
    for tag in ["br", "hr"]:
        assert Component(tag).render() == f"<{tag} />"


def test_form_helper():
    out = Form(Input(type="hidden"), class_="sortable").render()
    assert out.startswith('<form class="sortable"><input type="hidden" />')
