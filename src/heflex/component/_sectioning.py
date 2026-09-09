"""Content sectioning elements."""

from ._helper import Component


def Address(*children, **kwargs) -> Component:
    """Factory for the <address> element."""
    return Component("address", *children, **kwargs)


def Article(*children, **kwargs) -> Component:
    """Factory for the <article> element."""
    return Component("article", *children, **kwargs)


def Aside(*children, **kwargs) -> Component:
    """Factory for the <aside> element."""
    return Component("aside", *children, **kwargs)


def Footer(*children, **kwargs) -> Component:
    """Factory for the <footer> element."""
    return Component("footer", *children, **kwargs)


def Header(*children, **kwargs) -> Component:
    """Factory for the <header> element."""
    return Component("header", *children, **kwargs)


def H1(*children, **kwargs) -> Component:
    """Factory for the <h1> element."""
    return Component("h1", *children, **kwargs)


def H2(*children, **kwargs) -> Component:
    """Factory for the <h2> element."""
    return Component("h2", *children, **kwargs)


def H3(*children, **kwargs) -> Component:
    """Factory for the <h3> element."""
    return Component("h3", *children, **kwargs)


def H4(*children, **kwargs) -> Component:
    """Factory for the <h4> element."""
    return Component("h4", *children, **kwargs)


def H5(*children, **kwargs) -> Component:
    """Factory for the <h5> element."""
    return Component("h5", *children, **kwargs)


def H6(*children, **kwargs) -> Component:
    """Factory for the <h6> element."""
    return Component("h6", *children, **kwargs)


def Hgroup(*children, **kwargs) -> Component:
    """Factory for the <hgroup> element."""
    return Component("hgroup", *children, **kwargs)


def Main(*children, **kwargs) -> Component:
    """Factory for the <main> element."""
    return Component("main", *children, **kwargs)


def Nav(*children, **kwargs) -> Component:
    """Factory for the <nav> element."""
    return Component("nav", *children, **kwargs)


def Section(*children, **kwargs) -> Component:
    """Factory for the <section> element."""
    return Component("section", *children, **kwargs)


def Search(*children, **kwargs) -> Component:
    """Factory for the <search> element."""
    return Component("search", *children, **kwargs)
