"""Ports: the interfaces the core needs the outside world to implement.

Adapters (a SQL database, an in-memory store, a remote API) live *outside* the
core and satisfy these Protocols. The core depends on the interface, never on a
concrete implementation.
"""

from __future__ import annotations

from typing import Protocol

from ..domain.note import Note


class NoteRepository(Protocol):
    def add(self, note: Note) -> None: ...

    def list(self) -> list[Note]: ...

    def get(self, note_id: str) -> Note | None: ...
