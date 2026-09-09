"""Table elements."""

from ._helper import Component


def Caption(*children, **kwargs) -> Component:
    """Factory for the <caption> element."""
    return Component("caption", *children, **kwargs)


def Col(*children, **kwargs) -> Component:
    """Factory for the <col> element."""
    return Component("col", *children, **kwargs)


def Colgroup(*children, **kwargs) -> Component:
    """Factory for the <colgroup> element."""
    return Component("colgroup", *children, **kwargs)


def Table(*children, **kwargs) -> Component:
    """Factory for the <table> element."""
    return Component("table", *children, **kwargs)


def Tbody(*children, **kwargs) -> Component:
    """Factory for the <tbody> element."""
    return Component("tbody", *children, **kwargs)


def Td(*children, **kwargs) -> Component:
    """Factory for the <td> element."""
    return Component("td", *children, **kwargs)


def Tfoot(*children, **kwargs) -> Component:
    """Factory for the <tfoot> element."""
    return Component("tfoot", *children, **kwargs)


def Th(*children, **kwargs) -> Component:
    """Factory for the <th> element."""
    return Component("th", *children, **kwargs)


def Thead(*children, **kwargs) -> Component:
    """Factory for the <thead> element."""
    return Component("thead", *children, **kwargs)


def Tr(*children, **kwargs) -> Component:
    """Factory for the <tr> element."""
    return Component("tr", *children, **kwargs)
