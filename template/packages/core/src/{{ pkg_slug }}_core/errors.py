"""Domain-level errors. Adapters translate these into HTTP codes, exit codes, etc."""

from __future__ import annotations


class CoreError(Exception):
    """Base class for all domain errors raised by the core."""


# [demo] Sample-domain errors — replace alongside the Resource Vault domain.


class NoteNotFoundError(CoreError):
    def __init__(self, note_id: str) -> None:
        super().__init__(f"Note not found: {note_id}")
        self.note_id = note_id


class ProjectNotFoundError(CoreError):
    def __init__(self, project_id: str) -> None:
        super().__init__(f"Project not found: {project_id}")
        self.project_id = project_id
