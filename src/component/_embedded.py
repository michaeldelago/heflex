"""Embedded content elements."""

from ._helper import Component


def Embed(*children, **kwargs) -> Component:
    """Factory for the <embed> element."""
    return Component("embed", *children, **kwargs)


def Iframe(*children, **kwargs) -> Component:
    """Factory for the <iframe> element."""
    return Component("iframe", *children, **kwargs)


def Image(*children, **kwargs) -> Component:
    """Factory for the SVG <image> element."""
    return Component("image", *children, **kwargs)


def Math(*children, **kwargs) -> Component:
    """Factory for the <math> (MathML) element."""
    return Component("math", *children, **kwargs)


def Object(*children, **kwargs) -> Component:
    """Factory for the <object> element."""
    return Component("object", *children, **kwargs)


def Param(*children, **kwargs) -> Component:
    """Factory for the <param> element."""
    return Component("param", *children, **kwargs)


def Picture(*children, **kwargs) -> Component:
    """Factory for the <picture> element."""
    return Component("picture", *children, **kwargs)


def Svg(*children, **kwargs) -> Component:
    """Factory for the <svg> element."""
    return Component("svg", *children, **kwargs)
