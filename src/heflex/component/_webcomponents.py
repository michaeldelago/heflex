"""Web component elements."""

from ._helper import Component


def Slot(*children, **kwargs) -> Component:
    """Factory for the <slot> element."""
    return Component("slot", *children, **kwargs)


def Template(*children, **kwargs) -> Component:
    """Factory for the <template> element."""
    return Component("template", *children, **kwargs)
