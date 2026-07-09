# [demo] Resource Vault sample domain — replace with your product's services (see AGENTS.md).
"""Note use-cases, expressed against ports only."""

from __future__ import annotations

from collections.abc import Iterable

from ..domain.note import Note, normalize_tags
from ..errors import NoteNotFoundError, ProjectNotFoundError
from ..ports.repository import NoteRepository, ProjectRepository


class NoteService:
    def __init__(self, notes: NoteRepository, projects: ProjectRepository) -> None:
        self._notes = notes
        self._projects = projects

    def create(
        self,
        project_id: str,
        title: str,
        body: str = "",
        tags: Iterable[str] | None = None,
    ) -> Note:
        if self._projects.get(project_id) is None:
            raise ProjectNotFoundError(project_id)
        note = Note(
            project_id=project_id,
            title=title,
            body=body,
            tags=normalize_tags(tags),
        )
        self._notes.add(note)
        return note

    def get(self, note_id: str) -> Note:
        note = self._notes.get(note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note

    def search(
        self,
        *,
        project_id: str | None = None,
        tag: str | None = None,
        query: str | None = None,
    ) -> list[Note]:
        normalized_tag = tag.strip().lower() if tag else None
        return self._notes.list(
            project_id=project_id or None,
            tag=normalized_tag,
            query=query or None,
        )
