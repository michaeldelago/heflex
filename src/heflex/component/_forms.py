"""Form elements."""

from ._helper import Component


def Button(*children, **kwargs) -> Component:
    """Factory for the <button> element."""
    return Component("button", *children, **kwargs)


def Datalist(*children, **kwargs) -> Component:
    """Factory for the <datalist> element."""
    return Component("datalist", *children, **kwargs)


def Fieldset(*children, **kwargs) -> Component:
    """Factory for the <fieldset> element."""
    return Component("fieldset", *children, **kwargs)


def Form(*children, **kwargs) -> Component:
    """Factory for the <form> element."""
    return Component("form", *children, **kwargs)


def Input(*children, **kwargs) -> Component:
    """Factory for the <input> element."""
    return Component("input", *children, **kwargs)


def Label(*children, **kwargs) -> Component:
    """Factory for the <label> element."""
    return Component("label", *children, **kwargs)


def Legend(*children, **kwargs) -> Component:
    """Factory for the <legend> element."""
    return Component("legend", *children, **kwargs)


def Optgroup(*children, **kwargs) -> Component:
    """Factory for the <optgroup> element."""
    return Component("optgroup", *children, **kwargs)


def Option(*children, **kwargs) -> Component:
    """Factory for the <option> element."""
    return Component("option", *children, **kwargs)


def Meter(*children, **kwargs) -> Component:
    """Factory for the <meter> element."""
    return Component("meter", *children, **kwargs)


def Output(*children, **kwargs) -> Component:
    """Factory for the <output> element."""
    return Component("output", *children, **kwargs)


def Progress(*children, **kwargs) -> Component:
    """Factory for the <progress> element."""
    return Component("progress", *children, **kwargs)


def Select(*children, **kwargs) -> Component:
    """Factory for the <select> element."""
    return Component("select", *children, **kwargs)


def Textarea(*children, **kwargs) -> Component:
    """Factory for the <textarea> element."""
    return Component("textarea", *children, **kwargs)
