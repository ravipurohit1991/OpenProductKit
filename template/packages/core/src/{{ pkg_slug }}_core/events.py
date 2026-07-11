"""In-process events: how the core reports progress without knowing who listens.

An `Event` is a tiny publish/subscribe primitive for long-running core services
(progress, status, results). It keeps the core headless: services emit, and any
adapter — CLI, web, desktop — subscribes.

GUI toolkits require handlers to run on their main thread. Instead of the core
importing a toolkit, the *shell* installs a dispatcher once at startup:

    # in a Qt shell
    set_event_dispatcher(qt_dispatcher)   # marshals handlers onto the GUI thread

With no dispatcher installed (CLI, tests, servers), handlers run synchronously
on the emitting thread. Either way, the emitting code is identical.

This is deliberately not an async framework: no queues, no replay, no
priorities. If you outgrow it, replace the dispatcher — the emit sites stay.
"""

from __future__ import annotations

import logging
import threading
from collections.abc import Callable
from typing import Any

logger = logging.getLogger(__name__)

#: A dispatcher receives (handler, args) and decides where/when to call it.
Dispatcher = Callable[[Callable[..., Any], tuple[Any, ...]], None]

_dispatcher: Dispatcher | None = None
_dispatcher_lock = threading.Lock()


def set_event_dispatcher(dispatcher: Dispatcher | None) -> None:
    """Install a process-wide dispatcher (None restores synchronous delivery)."""
    global _dispatcher
    with _dispatcher_lock:
        _dispatcher = dispatcher


def get_event_dispatcher() -> Dispatcher | None:
    return _dispatcher


class Event:
    """A named, thread-safe pub/sub event.

    >>> progress = Event("indexing.progress")
    >>> off = progress.subscribe(lambda pct: print(pct))
    >>> progress.emit(42)
    42
    >>> off()  # unsubscribe
    """

    def __init__(self, name: str = "") -> None:
        self.name = name
        self._handlers: list[Callable[..., Any]] = []
        self._lock = threading.Lock()

    def subscribe(self, handler: Callable[..., Any]) -> Callable[[], None]:
        """Register `handler`; returns a zero-arg callable that unsubscribes it."""
        with self._lock:
            self._handlers.append(handler)

        def unsubscribe() -> None:
            with self._lock:
                try:
                    self._handlers.remove(handler)
                except ValueError:
                    pass  # already unsubscribed

        return unsubscribe

    def emit(self, *args: Any) -> None:
        """Call every handler with `args`, via the dispatcher when one is set.

        A failing handler is logged and skipped — an observer must never be
        able to break the service that is emitting.
        """
        with self._lock:
            handlers = list(self._handlers)
        dispatcher = _dispatcher
        for handler in handlers:
            try:
                if dispatcher is not None:
                    dispatcher(handler, args)
                else:
                    handler(*args)
            except Exception:  # noqa: BLE001 - see docstring
                logger.exception("Event %r handler %r failed", self.name, handler)

    def __repr__(self) -> str:  # pragma: no cover
        return f"Event({self.name!r}, handlers={len(self._handlers)})"
