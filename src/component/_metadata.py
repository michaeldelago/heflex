"""Document metadata elements."""

from ._helper import Component


def Base(*children, **kwargs) -> Component:
    """Factory for the <base> element."""
    return Component("base", *children, **kwargs)


def Head(*children, **kwargs) -> Component:
    """Factory for the <head> metadata container."""
    return Component("head", *children, **kwargs)


def Link(*children, **kwargs) -> Component:
    """Factory for the <link> element."""
    return Component("link", *children, **kwargs)


def Meta(*children, **kwargs) -> Component:
    """Factory for the <meta> element."""
    return Component("meta", *children, **kwargs)


def Title(*children, **kwargs) -> Component:
    """Factory for the <title> element."""
    return Component("title", *children, **kwargs)
