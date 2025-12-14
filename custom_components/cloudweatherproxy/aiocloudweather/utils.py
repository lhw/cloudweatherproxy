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
