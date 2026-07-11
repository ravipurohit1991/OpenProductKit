"""Marshals core events onto the Qt main thread.

The core's event bus (`events.set_event_dispatcher`) is toolkit-agnostic; this
is the Qt implementation of its `Dispatcher` contract. A queued Qt signal is
the standard thread-safe hand-off: `dispatch()` may be called from any worker
thread, the connected slot always runs on the thread that owns this QObject —
create it on the main thread, before any worker starts.
"""

from __future__ import annotations

from collections.abc import Callable
from typing import Any

from PySide6.QtCore import QObject, Qt, Signal


class QtEventDispatcher(QObject):
    _relay = Signal(object, object)

    def __init__(self, parent: QObject | None = None) -> None:
        super().__init__(parent)
        self._relay.connect(self._invoke, Qt.ConnectionType.QueuedConnection)

    def dispatch(self, handler: Callable[..., Any], args: tuple[Any, ...]) -> None:
        """Core-facing entry point: safe to call from any thread."""
        self._relay.emit(handler, args)

    def _invoke(self, handler: Callable[..., Any], args: tuple[Any, ...]) -> None:
        handler(*args)
