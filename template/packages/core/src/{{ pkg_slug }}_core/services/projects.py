# [demo] Resource Vault sample domain — replace with your product's services (see AGENTS.md).
"""Project use-cases, expressed against ports only."""

from __future__ import annotations

from ..domain.project import Project
from ..errors import ProjectNotFoundError
from ..ports.repository import ProjectRepository


class ProjectService:
    def __init__(self, repo: ProjectRepository) -> None:
        self._repo = repo

    def create(self, name: str) -> Project:
        project = Project(name=name)
        self._repo.add(project)
        return project

    def list(self) -> list[Project]:
        return self._repo.list()

    def get(self, project_id: str) -> Project:
        project = self._repo.get(project_id)
        if project is None:
            raise ProjectNotFoundError(project_id)
        return project
