"""Ports: the interfaces the core needs the outside world to implement.

Adapters (a SQL database, an in-memory store, a remote API) live *outside* the
core and satisfy these Protocols. The core depends on the interface, never on a
concrete implementation.
"""

from __future__ import annotations

from typing import Protocol

from ..domain.note import Note
from ..domain.project import Project


class ProjectRepository(Protocol):
    def add(self, project: Project) -> None: ...

    def list(self) -> list[Project]: ...

    def get(self, project_id: str) -> Project | None: ...


class NoteRepository(Protocol):
    def add(self, note: Note) -> None: ...

    def get(self, note_id: str) -> Note | None: ...

    def list(
        self,
        *,
        project_id: str | None = None,
        tag: str | None = None,
        query: str | None = None,
    ) -> list[Note]:
        """Return notes, optionally filtered by project, tag and free-text query."""
        ...
