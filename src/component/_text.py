"""Text content elements."""

from ._helper import Component


def Blockquote(*children, **kwargs) -> Component:
    """Factory for the <blockquote> element."""
    return Component("blockquote", *children, **kwargs)


def Dd(*children, **kwargs) -> Component:
    """Factory for the <dd> element."""
    return Component("dd", *children, **kwargs)


def Div(*children, **kwargs) -> Component:
    """Factory for the <div> element."""
    return Component("div", *children, **kwargs)


def Dl(*children, **kwargs) -> Component:
    """Factory for the <dl> element."""
    return Component("dl", *children, **kwargs)


def Dt(*children, **kwargs) -> Component:
    """Factory for the <dt> element."""
    return Component("dt", *children, **kwargs)


def Figcaption(*children, **kwargs) -> Component:
    """Factory for the <figcaption> element."""
    return Component("figcaption", *children, **kwargs)


def Figure(*children, **kwargs) -> Component:
    """Factory for the <figure> element."""
    return Component("figure", *children, **kwargs)


def Hr(*children, **kwargs) -> Component:
    """Factory for the <hr> element."""
    return Component("hr", *children, **kwargs)


def Li(*children, **kwargs) -> Component:
    """Factory for the <li> element."""
    return Component("li", *children, **kwargs)


def Menu(*children, **kwargs) -> Component:
    """Factory for the <menu> element."""
    return Component("menu", *children, **kwargs)


def Ol(*children, **kwargs) -> Component:
    """Factory for the <ol> element."""
    return Component("ol", *children, **kwargs)


def P(*children, **kwargs) -> Component:
    """Factory for the <p> element."""
    return Component("p", *children, **kwargs)


def Pre(*children, **kwargs) -> Component:
    """Factory for the <pre> element."""
    return Component("pre", *children, **kwargs)


def Ul(*children, **kwargs) -> Component:
    """Factory for the <ul> element."""
    return Component("ul", *children, **kwargs)
