"""Utilities for aiocloudweather.

This module provides two small helpers used across the package:
- `LimitedSizeQueue`: a simple asyncio.Queue variant that discards the
  oldest item when full.
- `resolve_caster` / `cast_value`: helpers to resolve typing hints
  (including Optional/Union) into a usable caster and cast values
  extracted from incoming requests.
"""

import asyncio
import contextlib
import logging
import re
from typing import Any, get_args
from collections.abc import Callable


class LimitedSizeQueue(asyncio.Queue):
    """Queue with fixed maximum size that drops oldest items when full.

    This is a tiny convenience used for in-memory log buffering.
    """

    def put_nowait(self, item: Any) -> None:
        """Put `item` without blocking; drop oldest when the queue is full."""
        if self.full():
            with contextlib.suppress(Exception):
                self.get_nowait()
        super().put_nowait(item)


# Public, shared in-memory log buffer for diagnostics.
# Size chosen conservatively; integration also creates a smaller per-HASS queue.
LOG_BUFFER: LimitedSizeQueue = LimitedSizeQueue(maxsize=500)


def _mask_credentials(text: str) -> str:
    """Mask known credential patterns in `text` for diagnostics.

    - Replaces query parameters `ID` and `PASSWORD` with a fixed placeholder.
    - Replaces path segments `wid/<val>` and `key/<val>` with standardized values.
    - Replaces station IDs in log messages (e.g., "Found new station: xyz").
    """
    # Replace query params like ID=... and PASSWORD=...
    text = re.sub(r"(?i)(ID)=([^&\s]+)", r"\1=<REMOVED>", text)
    text = re.sub(r"(?i)(PASSWORD)=([^&\s]+)", r"\1=<REMOVED>", text)

    # Replace path segments like /wid/<val>/ and /key/<val>/
    text = re.sub(r"(?i)(/wid/)[^/\\s]+", r"\1" + "<REMOVED>", text)
    text = re.sub(r"(?i)(/key/)[^/\\s]+", r"\1" + "<REMOVED>", text)

    # Replace station IDs in log messages like "Found new station: <id>"
    text = re.sub(r"(?i)(station:\s+)([^\s]+)", r"\g<1><REMOVED>", text)

    return text


class DiagnosticsLogHandler(logging.Handler):
    """Logging handler that writes formatted, masked messages into a queue.

    The handler accepts an asyncio-compatible queue (implements `put_nowait`).
    """

    def __init__(self, queue: LimitedSizeQueue | None = None) -> None:
        super().__init__()
        self.queue = queue or LOG_BUFFER
        # Use a simple formatter if none provided
        self.setFormatter(logging.Formatter(
            "%(asctime)s %(levelname)s %(name)s: %(message)s"))

    def emit(self, record: logging.LogRecord) -> None:
        try:
            msg = self.format(record)
            msg = _mask_credentials(msg)
            # store the masked, formatted message
            with contextlib.suppress(Exception):
                # put_nowait will drop oldest when full
                self.queue.put_nowait(msg)
        except Exception:
            # Ensure logging doesn't raise
            self.handleError(record)


def get_buffered_logs(max_items: int | None = None) -> list[str]:
    """Return a snapshot of buffered log lines.

    Does not consume the buffer. If `max_items` is provided, returns only
    the most recent N entries.
    """
    q = LOG_BUFFER
    # Access underlying deque of asyncio.Queue
    items = list(getattr(q, "_queue", []))
    if max_items is not None:
        return items[-max_items:]
    return items


def resolve_caster(type_hint: Any) -> Any:
    """Resolve a usable caster from a typing hint.

    Handles Optional/Union (PEP 604) by selecting the first non-None
    alternative. Returns the resolved type/caster; callers may check
    `callable()` on the result to determine if it can be invoked.
    """
    args = get_args(type_hint)
    if args:
        non_none = [t for t in args if t is not type(None)]
        return non_none[0] if non_none else args[0]
    return type_hint


def cast_value(type_hint: Any, value: Any) -> Any:
    """Cast `value` according to `type_hint` when possible.

    If the resolved caster is callable, it will be called with `value`.
    On any exception the original `value` is returned so callers can
    decide how to handle casting failures.
    """
    caster: Callable[..., Any] | None = resolve_caster(type_hint)
    try:
        if callable(caster):
            return caster(value)
    except Exception:
        # Caller will log casting/validation failures; fall back to raw value
        pass
    return value
