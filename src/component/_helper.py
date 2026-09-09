"""
Core Component class and RawHTML marker.

These are the building blocks that every element factory function returns.
"""

import html as _html
from dataclasses import dataclass
from typing import Any, Mapping, Iterable

# Tags whose text content browsers parse as raw text (no entity decoding).
_RAW_CONTENT_TAGS = {"script", "style"}


class RawHTML:
    """Pre-built HTML that should be interpolated verbatim, without escaping."""

    __slots__ = ("content",)

    def __init__(self, content: str):
        self.content = content

    def render(self) -> str:
        return self.content


@dataclass
class Component:
    tag: str
    children: list[str | Component]
    attributes: Mapping[str, Any]

    def __init__(self, tag: str, *children, **attributes):
        self.tag = tag
        self.children = list(children)
        self.attributes = attributes

    def _render_style(self, style: Mapping[str, Any]):
        style_value = "; ".join([f"{k.strip()}: {v.strip()}" for k, v in style.items()])
        return f'style="{_html.escape(style_value, quote=True)}"'

    @staticmethod
    def _render_attr_name(key: str) -> str:
        """
        Convert Python snake_case kwargs to HTML attribute names.

        e.g., hx_get="/path" -> hx-get="/path"

        A single trailing underscore is stripped (e.g. class_="foo"). To emit
        a name ending in a literal underscore, double it: data_foo__=...
        renders data-foo_. All other underscores become hyphens.
        """
        if key.endswith("__"):
            return key[:-2].replace("_", "-") + "_"
        if key.endswith("_"):
            key = key[:-1]
        return key.replace("_", "-")

    def _render_attr(self, key: str, val: Any) -> str:
        """
        Render one attribute; values are always HTML-escaped and booleans
        render as attr="true" (HTMX v4 spec) or are omitted when False.
        """
        attr_name = self._render_attr_name(key)
        if isinstance(val, bool):
            return f'{attr_name}="true"' if val else ""
        return f'{attr_name}="{_html.escape(str(val), quote=True)}"'

    def _render_child(self, child) -> str:
        if isinstance(child, Component):
            return child.render()
        if isinstance(child, RawHTML):
            return child.content
        text = str(child)
        # script/style content is raw text to browsers; escaping would break it.
        if self.tag in _RAW_CONTENT_TAGS:
            return text
        return _html.escape(text)

    def render(self) -> str:
        rendered_attrs = []
        for k, v in self.attributes.items():
            if isinstance(v, bool) and not v:
                continue
            if k == "style":
                rendered_attrs.append(self._render_style(v))
                continue

            rendered_attrs.append(self._render_attr(k, v))

        attr_str = ""
        if rendered_attrs:
            attr_str = f" {" ".join(rendered_attrs)}"

        # Self-closing tags handling
        if self.tag in ["input", "img", "br", "hr", "meta"]:
            return f"<{self.tag}{attr_str} />"

        rendered_children = "".join(self._render_child(child) for child in self.children)
        return f"<{self.tag}{attr_str}>{rendered_children}</{self.tag}>"
