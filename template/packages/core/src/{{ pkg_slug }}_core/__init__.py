"""Pure domain core: models, ports and services with no I/O dependencies."""

# [demo] Everything re-exported here except CoreError belongs to the Resource
# Vault sample domain — swap these for your own exports.
from .domain.note import Note, normalize_tags
from .domain.project import Project
from .errors import (
    CoreError,
    NoteNotFoundError,
    ProjectNotFoundError,
)
from .ports.repository import NoteRepository, ProjectRepository
from .services.notes import NoteService
from .services.projects import ProjectService

__all__ = [
    "Note",
    "Project",
    "normalize_tags",
    "NoteRepository",
    "ProjectRepository",
    "NoteService",
    "ProjectService",
    "CoreError",
    "NoteNotFoundError",
    "ProjectNotFoundError",
]
