"""Pure domain core: models, ports and services with no I/O dependencies."""

from .domain.note import Note
from .errors import CoreError, NoteNotFoundError
from .ports.repository import NoteRepository
from .services.notes import NoteService

__all__ = [
    "Note",
    "NoteRepository",
    "NoteService",
    "CoreError",
    "NoteNotFoundError",
]
