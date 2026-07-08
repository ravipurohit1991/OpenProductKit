"""Application services: the use-cases, expressed against ports only."""

from __future__ import annotations

from ..domain.note import Note
from ..errors import NoteNotFoundError
from ..ports.repository import NoteRepository


class NoteService:
    def __init__(self, repo: NoteRepository) -> None:
        self._repo = repo

    def create(self, title: str, body: str = "") -> Note:
        note = Note(title=title, body=body)
        self._repo.add(note)
        return note

    def list(self) -> list[Note]:
        return self._repo.list()

    def get(self, note_id: str) -> Note:
        note = self._repo.get(note_id)
        if note is None:
            raise NoteNotFoundError(note_id)
        return note
