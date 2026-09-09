"""
heflex.component — HTML element factory functions.

Organized by semantic category. Each module exports factory functions that
produce ``Component(tag, *children, **attributes)`` instances.

Import everything from the top-level package::

    from component import Div, Button, Input, Form, A, Span, ...

Or import by category::

    from component.forms import Button, Input, Select, ...
"""

# Root elements
from ._root import Html, Body

# Document metadata
from ._metadata import Base, Head, Link, Meta, Title

# Content sectioning
from ._sectioning import (
    Address, Article, Aside, Footer, Header, H1, H2, H3, H4, H5, H6,
    Hgroup, Main, Nav, Section, Search,
)

# Text content
from ._text import (
    Blockquote, Dd, Div, Dl, Dt, Figcaption, Figure, Hr, Li, Menu, Ol,
    P, Pre, Ul,
)

# Inline text semantics
from ._inline import (
    A, Abbr, B, Bdi, Bdo, Br, Cite, Code, Data, Dfn, Del, Em, I, Ins, Kbd,
    Mark, Q, Rb, Rp, Rt, Rtc, Ruby, S, Samp, Small, Span, Strong, Sub, Sup,
    Time, U, Var, Wbr,
)

# Image and multimedia
from ._media import Area, Audio, Canvas, Img, Map, Source, Track, Video

# Embedded content
from ._embedded import Embed, Iframe, Image, Math, Object, Param, Picture, Svg

# Table elements
from ._table import Caption, Col, Colgroup, Table, Tbody, Td, Tfoot, Th, Thead, Tr

# Form elements
from ._forms import (
    Button, Datalist, Fieldset, Form, Input, Label, Legend, Meter, Optgroup,
    Option, Output, Progress, Select, Textarea,
)

# Interactive elements
from ._interactive import Details, Dialog, Summary

# Web components
from ._webcomponents import Slot, Template

# Special handling
from ._helper import Component, RawHTML
from ._special import Script, Style

# Deprecated / obsolete elements
from . import deprecated  # noqa: F401

__all__ = [
    # Root
    "Html", "Body",
    # Metadata
    "Base", "Head", "Link", "Meta", "Title",
    # Sectioning
    "Address", "Article", "Aside", "Footer", "Header", "H1", "H2", "H3",
    "H4", "H5", "H6", "Hgroup", "Main", "Nav", "Section", "Search",
    # Text content
    "Blockquote", "Dd", "Div", "Dl", "Dt", "Figcaption", "Figure", "Hr",
    "Li", "Menu", "Ol", "P", "Pre", "Ul",
    # Inline text semantics
    "A", "Abbr", "B", "Bdi", "Bdo", "Br", "Cite", "Code", "Data", "Dfn",
    "Del", "Em", "I", "Ins", "Kbd", "Mark", "Q", "Rb", "Rp", "Rt", "Rtc",
    "Ruby", "S", "Samp", "Small", "Span", "Strong", "Sub", "Sup", "Time",
    "U", "Var", "Wbr",
    # Image and multimedia
    "Area", "Audio", "Canvas", "Img", "Map", "Source", "Track", "Video",
    # Embedded content
    "Embed", "Iframe", "Image", "Math", "Object", "Param", "Picture", "Svg",
    # Table elements
    "Caption", "Col", "Colgroup", "Table", "Tbody", "Td", "Tfoot", "Th", "Thead", "Tr",
    # Form elements
    "Button", "Datalist", "Fieldset", "Form", "Input", "Label", "Legend", "Meter",
    "Optgroup", "Option", "Output", "Progress", "Select", "Textarea",
    # Interactive
    "Details", "Dialog", "Summary",
    # Web components
    "Slot", "Template",
    # Special
    "Component", "RawHTML", "Script", "Style",
]
