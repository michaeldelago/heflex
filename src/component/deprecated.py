"""
Deprecated and obsolete HTML element factories.

These elements are deprecated, obsolete, or experimental in modern HTML.
They are provided for backward compatibility with legacy content.

.. deprecated::
    Use modern alternatives instead. These elements may be removed in a future
    release.
"""

import warnings
from typing import Any

from ._helper import Component

# Mapping of deprecated tag names to their modern alternatives (where applicable)
_DEPRECATED_INFO = {
    "acronym": "Use <abbr> instead",
    "big": "Use CSS font-size instead",
    "center": "Use CSS text-align or flexbox instead",
    "content": "Use <slot> (Shadow DOM) instead",
    "dir": "Use <ul> instead",
    "fencedframe": "Use <iframe> with appropriate sandbox attributes",
    "font": "Use CSS font properties instead",
    "frame": "Use <iframe> instead",
    "frameset": "Use CSS flexbox/grid instead",
    "geolocation": "No direct replacement; use the Geolocation API",
    "marquee": "Use CSS animations instead",
    "menuitem": "Use a <button> or <a> inside a <menu> instead",
    "nobr": "Use CSS white-space: nowrap instead",
    "noembed": "Use <noscript> or modern fallback strategies",
    "noframes": "Use progressive enhancement; <frameset> is obsolete",
    "noscript": "Use progressive enhancement; handle in JS",
    "plaintext": "Use a <textarea readonly> or <pre> instead",
    "selectedcontent": "Use <slot> (Shadow DOM) instead",
    "shadow": "Use Shadow DOM (custom elements) instead",
    "strike": "Use <s> or <del> instead",
    "tt": "Use CSS font-family instead",
    "xmp": "Use <pre> instead",
}


def _deprecated_factory(tag: str, *children, **kwargs) -> Component:
    """Factory that wraps Component and emits a deprecation warning."""
    info = _DEPRECATED_INFO.get(tag)
    if info:
        warnings.warn(
            f"<{tag}> is deprecated. {info}",
            DeprecationWarning,
            stacklevel=2,
        )
    return Component(tag, *children, **kwargs)


# ── Deprecated text/inline elements ──────────────────────────────────


def Acronym(*children, **kwargs) -> Component:
    """Factory for the deprecated <acronym> element.

    .. deprecated::
        Use <abbr> instead.
    """
    return _deprecated_factory("acronym", *children, **kwargs)


def Big(*children, **kwargs) -> Component:
    """Factory for the deprecated <big> element.

    .. deprecated::
        Use CSS font-size instead.
    """
    return _deprecated_factory("big", *children, **kwargs)


def Strike(*children, **kwargs) -> Component:
    """Factory for the deprecated <strike> element.

    .. deprecated::
        Use <s> or <del> instead.
    """
    return _deprecated_factory("strike", *children, **kwargs)


def Tt(*children, **kwargs) -> Component:
    """Factory for the deprecated <tt> element.

    .. deprecated::
        Use CSS font-family instead.
    """
    return _deprecated_factory("tt", *children, **kwargs)


# ── Deprecated block/structural elements ─────────────────────────────


def Center(*children, **kwargs) -> Component:
    """Factory for the deprecated <center> element.

    .. deprecated::
        Use CSS text-align or flexbox instead.
    """
    return _deprecated_factory("center", *children, **kwargs)


def Dir(*children, **kwargs) -> Component:
    """Factory for the deprecated <dir> element.

    .. deprecated::
        Use <ul> instead.
    """
    return _deprecated_factory("dir", *children, **kwargs)


def Font(*children, **kwargs) -> Component:
    """Factory for the deprecated <font> element.

    .. deprecated::
        Use CSS font properties instead.
    """
    return _deprecated_factory("font", *children, **kwargs)


# ── Deprecated frame/frameset elements ───────────────────────────────


def Frame(*children, **kwargs) -> Component:
    """Factory for the deprecated <frame> element.

    .. deprecated::
        Use <iframe> instead.
    """
    return _deprecated_factory("frame", *children, **kwargs)


def Frameset(*children, **kwargs) -> Component:
    """Factory for the deprecated <frameset> element.

    .. deprecated::
        Use CSS flexbox/grid instead.
    """
    return _deprecated_factory("frameset", *children, **kwargs)


# ── Deprecated/obsolete conditional elements ─────────────────────────


def Noembed(*children, **kwargs) -> Component:
    """Factory for the obsolete <noembed> element.

    .. deprecated::
        Use <noscript> or modern fallback strategies.
    """
    return _deprecated_factory("noembed", *children, **kwargs)


def Noframes(*children, **kwargs) -> Component:
    """Factory for the obsolete <noframes> element.

    .. deprecated::
        Use progressive enhancement; <frameset> is obsolete.
    """
    return _deprecated_factory("noframes", *children, **kwargs)


def Noscript(*children, **kwargs) -> Component:
    """Factory for the <noscript> element.

    .. deprecated::
        Use progressive enhancement; handle in JS.
    """
    return _deprecated_factory("noscript", *children, **kwargs)


# ── Obsolete Shadow DOM elements ─────────────────────────────────────


def Content(*children, **kwargs) -> Component:
    """Factory for the obsolete <content> element (Shadow DOM v0).

    .. deprecated::
        Use <slot> (Shadow DOM v1) instead.
    """
    return _deprecated_factory("content", *children, **kwargs)


def Selectedcontent(*children, **kwargs) -> Component:
    """Factory for the obsolete <selectedcontent> element.

    .. deprecated::
        Use <slot> (Shadow DOM v1) instead.
    """
    return _deprecated_factory("selectedcontent", *children, **kwargs)


def Shadow(*children, **kwargs) -> Component:
    """Factory for the obsolete <shadow> element (Shadow DOM v0).

    .. deprecated::
        Use Shadow DOM (custom elements) instead.
    """
    return _deprecated_factory("shadow", *children, **kwargs)


# ── Obsolete/legacy elements ─────────────────────────────────────────


def Geolocation(*children, **kwargs) -> Component:
    """Factory for the obsolete <geolocation> element.

    .. deprecated::
        No direct replacement; use the Geolocation API.
    """
    return _deprecated_factory("geolocation", *children, **kwargs)


def Marquee(*children, **kwargs) -> Component:
    """Factory for the obsolete <marquee> element.

    .. deprecated::
        Use CSS animations instead.
    """
    return _deprecated_factory("marquee", *children, **kwargs)


def Menuitem(*children, **kwargs) -> Component:
    """Factory for the deprecated <menuitem> element.

    .. deprecated::
        Use a <button> or <a> inside a <menu> instead.
    """
    return _deprecated_factory("menuitem", *children, **kwargs)


def Nobr(*children, **kwargs) -> Component:
    """Factory for the deprecated <nobr> element.

    .. deprecated::
        Use CSS white-space: nowrap instead.
    """
    return _deprecated_factory("nobr", *children, **kwargs)


def Plaintext(*children, **kwargs) -> Component:
    """Factory for the obsolete <plaintext> element.

    .. deprecated::
        Use a <textarea readonly> or <pre> instead.
    """
    return _deprecated_factory("plaintext", *children, **kwargs)


def Xmp(*children, **kwargs) -> Component:
    """Factory for the obsolete <xmp> element.

    .. deprecated::
        Use <pre> instead.
    """
    return _deprecated_factory("xmp", *children, **kwargs)


# ── Experimental elements ────────────────────────────────────────────


def Fencedframe(*children, **kwargs) -> Component:
    """Factory for the experimental <fencedframe> element.

    .. deprecated::
        Use <iframe> with appropriate sandbox attributes.
    """
    return _deprecated_factory("fencedframe", *children, **kwargs)


__all__ = [
    # Inline
    "Acronym", "Big", "Strike", "Tt",
    # Block/structural
    "Center", "Dir", "Font",
    # Frames
    "Frame", "Frameset",
    # Conditional
    "Noembed", "Noframes", "Noscript",
    # Shadow DOM
    "Content", "Selectedcontent", "Shadow",
    # Obsolete
    "Geolocation", "Marquee", "Menuitem", "Nobr", "Plaintext", "Xmp",
    # Experimental
    "Fencedframe",
]
