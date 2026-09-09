"""Root elements: <html> and <body>."""

from ._helper import Component


def Html(*children, **kwargs) -> Component:
    """Factory for the <html> root element."""
    return Component("html", *children, **kwargs)


def Body(*children, **kwargs) -> Component:
    """Factory for the <body> content root element."""
    return Component("body", *children, **kwargs)
