"""Inline text semantics elements."""

from ._helper import Component


def A(*children, **kwargs) -> Component:
    """Factory for the <a> element."""
    return Component("a", *children, **kwargs)


def Abbr(*children, **kwargs) -> Component:
    """Factory for the <abbr> element."""
    return Component("abbr", *children, **kwargs)


def B(*children, **kwargs) -> Component:
    """Factory for the <b> element."""
    return Component("b", *children, **kwargs)


def Bdi(*children, **kwargs) -> Component:
    """Factory for the <bdi> element."""
    return Component("bdi", *children, **kwargs)


def Bdo(*children, **kwargs) -> Component:
    """Factory for the <bdo> element."""
    return Component("bdo", *children, **kwargs)


def Br(*children, **kwargs) -> Component:
    """Factory for the <br> element."""
    return Component("br", *children, **kwargs)


def Del(*children, **kwargs) -> Component:
    """Factory for the <del> element."""
    return Component("del", *children, **kwargs)


def Ins(*children, **kwargs) -> Component:
    """Factory for the <ins> element."""
    return Component("ins", *children, **kwargs)


def Cite(*children, **kwargs) -> Component:
    """Factory for the <cite> element."""
    return Component("cite", *children, **kwargs)


def Code(*children, **kwargs) -> Component:
    """Factory for the <code> element."""
    return Component("code", *children, **kwargs)


def Data(*children, **kwargs) -> Component:
    """Factory for the <data> element."""
    return Component("data", *children, **kwargs)


def Dfn(*children, **kwargs) -> Component:
    """Factory for the <dfn> element."""
    return Component("dfn", *children, **kwargs)


def Em(*children, **kwargs) -> Component:
    """Factory for the <em> element."""
    return Component("em", *children, **kwargs)


def I(*children, **kwargs) -> Component:  # noqa: E743
    """Factory for the <i> element."""
    return Component("i", *children, **kwargs)


def Kbd(*children, **kwargs) -> Component:
    """Factory for the <kbd> element."""
    return Component("kbd", *children, **kwargs)


def Mark(*children, **kwargs) -> Component:
    """Factory for the <mark> element."""
    return Component("mark", *children, **kwargs)


def Q(*children, **kwargs) -> Component:
    """Factory for the <q> element."""
    return Component("q", *children, **kwargs)


def Rp(*children, **kwargs) -> Component:
    """Factory for the <rp> element."""
    return Component("rp", *children, **kwargs)


def Rb(*children, **kwargs) -> Component:
    """Factory for the <rb> element (ruby base)."""
    return Component("rb", *children, **kwargs)


def Rt(*children, **kwargs) -> Component:
    """Factory for the <rt> element (ruby text)."""
    return Component("rt", *children, **kwargs)


def Rtc(*children, **kwargs) -> Component:
    """Factory for the <rtc> element (ruby text container)."""
    return Component("rtc", *children, **kwargs)


def Ruby(*children, **kwargs) -> Component:
    """Factory for the <ruby> element."""
    return Component("ruby", *children, **kwargs)


def S(*children, **kwargs) -> Component:
    """Factory for the <s> element."""
    return Component("s", *children, **kwargs)


def Samp(*children, **kwargs) -> Component:
    """Factory for the <samp> element."""
    return Component("samp", *children, **kwargs)


def Small(*children, **kwargs) -> Component:
    """Factory for the <small> element."""
    return Component("small", *children, **kwargs)


def Span(*children, **kwargs) -> Component:
    """Factory for the <span> element."""
    return Component("span", *children, **kwargs)


def Strong(*children, **kwargs) -> Component:
    """Factory for the <strong> element."""
    return Component("strong", *children, **kwargs)


def Sub(*children, **kwargs) -> Component:
    """Factory for the <sub> element."""
    return Component("sub", *children, **kwargs)


def Sup(*children, **kwargs) -> Component:
    """Factory for the <sup> element."""
    return Component("sup", *children, **kwargs)


def Time(*children, **kwargs) -> Component:
    """Factory for the <time> element."""
    return Component("time", *children, **kwargs)


def U(*children, **kwargs) -> Component:
    """Factory for the <u> element."""
    return Component("u", *children, **kwargs)


def Var(*children, **kwargs) -> Component:
    """Factory for the <var> element."""
    return Component("var", *children, **kwargs)


def Wbr(*children, **kwargs) -> Component:
    """Factory for the <wbr> element."""
    return Component("wbr", *children, **kwargs)
