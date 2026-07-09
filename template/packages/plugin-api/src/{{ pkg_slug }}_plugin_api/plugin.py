"""The Plugin contract.

A plugin may contribute any subset of: backend routes, CLI commands, a settings
schema, admin nav items, and a health check. Everything except the manifest is
optional; the base returns "nothing" so plugins only override what they use.

Return types for the framework-specific hooks are quoted so this SDK carries no
runtime dependency on FastAPI or Typer — a plugin brings those itself if it uses
them.
"""

from __future__ import annotations

from abc import ABC, abstractmethod
from typing import TYPE_CHECKING, Any

from .health import HealthStatus
from .manifest import PluginManifest
from .nav import NavItem

if TYPE_CHECKING:
    import typer
    from fastapi import APIRouter


class Plugin(ABC):
    @property
    @abstractmethod
    def manifest(self) -> PluginManifest: ...

    def backend_router(self) -> APIRouter | None:
        """A FastAPI router to mount, or None."""
        return None

    def cli(self) -> typer.Typer | None:
        """A Typer app to attach to the CLI, or None."""
        return None

    def settings_schema(self) -> dict[str, Any] | None:
        """A JSON schema describing the plugin's settings, or None."""
        return None

    def nav_items(self) -> list[NavItem]:
        """Admin nav entries this plugin contributes."""
        return []

    def health(self) -> HealthStatus:
        """A cheap health probe surfaced in the plugin manager."""
        return HealthStatus.ok()
