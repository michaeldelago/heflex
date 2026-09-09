"""Image and multimedia elements."""

from ._helper import Component


def Area(*children, **kwargs) -> Component:
    """Factory for the <area> element."""
    return Component("area", *children, **kwargs)


def Audio(*children, **kwargs) -> Component:
    """Factory for the <audio> element."""
    return Component("audio", *children, **kwargs)


def Canvas(*children, **kwargs) -> Component:
    """Factory for the <canvas> element."""
    return Component("canvas", *children, **kwargs)


def Img(*children, **kwargs) -> Component:
    """Factory for the <img> element."""
    return Component("img", *children, **kwargs)


def Map(*children, **kwargs) -> Component:
    """Factory for the <map> element."""
    return Component("map", *children, **kwargs)


def Track(*children, **kwargs) -> Component:
    """Factory for the <track> element."""
    return Component("track", *children, **kwargs)


def Source(*children, **kwargs) -> Component:
    """Factory for the <source> element."""
    return Component("source", *children, **kwargs)


def Video(*children, **kwargs) -> Component:
    """Factory for the <video> element."""
    return Component("video", *children, **kwargs)
