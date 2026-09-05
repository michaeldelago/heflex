#!/usr/bin/env python3


from dataclasses import dataclass
from typing import Any, Mapping, Iterable


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
        return f'style="{style_value}"'

    def _render_attr(self, key: str, val: Any) -> str:
        """
        Convert Python snake_case to HTML/HTMX hyphenated attributes
        e.g., hx_get="/path" -> hx-get="/path"
        e.g., hx_inherited=True -> hx-inherited="true" (HTMX v4 spec)
        """
        attr_name = key.replace("_", "-")
        if isinstance(val, bool):
            return f'{attr_name}="true"' if val else ""
        return f'{attr_name}="{val}"'

    def render(self) -> str:
        rendered_attrs = []
        for k, v in self.attributes.items():
            if k == "style":
                rendered_attrs.append(self._render_style(v))
                continue

            if k.endswith("_"):
                k = k[:-1]

            rendered_attrs.append(self._render_attr(k, v))

        attr_str = ""
        if rendered_attrs:
            attr_str = f" {" ".join(rendered_attrs)}"

        # Self-closing tags handling
        if self.tag in ["input", "img", "br", "hr", "meta"]:
            return f"<{self.tag}{attr_str} />"

        rendered_children = "".join(
            child.render() if isinstance(child, Component) else str(child)
            for child in self.children
        )
        return f"<{self.tag}{attr_str}>{rendered_children}</{self.tag}>"


def Div(*children, **kwargs):
    return Component("div", *children, **kwargs)


def Button(*children, **kwargs):
    return Component("button", *children, **kwargs)


def Input(**kwargs):
    return Component("input", **kwargs)


def Form(*children, **kwargs):
    return Component("form", *children, **kwargs)


def Script(content: str, **kwargs):
    return Component("script", content, **kwargs)


def Style(content: str, **kwargs):
    return Component("style", content, **kwargs)
