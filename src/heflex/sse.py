#!/usr/bin/env python3

"""Server-Sent Events helpers for heflex route handlers.

Async-generator route handlers are streamed as ``text/event-stream``; every
yielded item is framed into an SSE message:

- ``Component`` / ``str`` / ``RawHTML``  -> unnamed event (the rendered or
  raw text is swapped by htmx's hx-sse extension like an HTML response)
- ``SSEEvent``                            -> explicit fields (event name, id,
  retry), used for named events, ``hx-sse:close`` triggers, and replay ids
"""

from dataclasses import dataclass


def _data_lines(text: str) -> list[str]:
    """Split text into SSE ``data:`` lines so the payload survives newlines."""
    return [f"data: {line}" if line else "data:" for line in text.split("\n")]


@dataclass
class SSEEvent:
    """One Server-Sent Event with explicit fields.

    ``event`` names the event (dispatches a DOM event / matches
    ``hx-sse:close``); omit it for an unnamed HTML-swapping message.
    """

    data: str = ""
    event: str | None = None
    id: str | None = None
    retry: int | None = None

    def frame(self) -> str:
        if self.event is not None and (
            "\n" in self.event or " " in self.event
        ):
            raise ValueError("SSE event names must not contain spaces or newlines")
        parts: list[str] = []
        if self.event is not None:
            parts.append(f"event: {self.event}")
        if self.id is not None:
            parts.append(f"id: {self.id}")
        if self.retry is not None:
            parts.append(f"retry: {self.retry}")
        parts.extend(_data_lines(self.data))
        return "\n".join(parts) + "\n\n"


def frame_item(item: object) -> str:
    """Frame one yielded item into a well-formed SSE message block."""
    from .component import Component, RawHTML

    if isinstance(item, SSEEvent):
        return item.frame()
    if isinstance(item, Component):
        text = item.render()
    elif isinstance(item, RawHTML):
        text = item.content
    elif isinstance(item, str):
        text = item
    else:
        raise TypeError(
            f"SSE handlers must yield Component, str, RawHTML, or SSEEvent; "
            f"got {type(item).__name__}"
        )
    return "\n".join(_data_lines(text)) + "\n\n"
