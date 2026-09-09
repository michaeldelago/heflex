"""Special elements with unique behavior."""

from ._helper import Component, RawHTML

# Tags whose text content browsers parse as raw text (no entity decoding).
_RAW_CONTENT_TAGS = {"script", "style"}


def Script(content: str, **kwargs) -> Component:
    """Factory for the <script> element.

    The *content* argument is passed as raw text (no HTML escaping).
    """
    return Component("script", content, **kwargs)


def Style(content: str, **kwargs) -> Component:
    """Factory for the <style> element.

    The *content* argument is passed as raw text (no HTML escaping).
    """
    return Component("style", content, **kwargs)
