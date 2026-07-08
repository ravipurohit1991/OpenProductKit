"""Domain-level errors. Adapters translate these into HTTP codes, exit codes, etc."""

from __future__ import annotations


class CoreError(Exception):
    """Base class for all domain errors raised by the core."""


class NoteNotFoundError(CoreError):
    def __init__(self, note_id: str) -> None:
        super().__init__(f"Note not found: {note_id}")
        self.note_id = note_id
