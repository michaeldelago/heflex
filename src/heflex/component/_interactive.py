"""Interactive elements."""

from ._helper import Component


def Details(*children, **kwargs) -> Component:
    """Factory for the <details> element."""
    return Component("details", *children, **kwargs)


def Dialog(*children, **kwargs) -> Component:
    """Factory for the <dialog> element."""
    return Component("dialog", *children, **kwargs)


def Summary(*children, **kwargs) -> Component:
    """Factory for the <summary> element."""
    return Component("summary", *children, **kwargs)
