"""Alembic-backed schema management.

Migrations are the single source of truth for the database schema (no more
`create_all`). The app applies them automatically on startup, and the CLI
exposes them via `opk db …`. Paths are resolved relative to this package so
they work for editable installs (dev) and the source-copied Docker image.
"""

from __future__ import annotations

from pathlib import Path

from alembic import command
from alembic.config import Config

from .settings import settings

_BACKEND_ROOT = Path(__file__).resolve().parents[2]  # apps/backend
_ALEMBIC_INI = _BACKEND_ROOT / "alembic.ini"
_MIGRATIONS = _BACKEND_ROOT / "migrations"


def _config() -> Config:
    if not _ALEMBIC_INI.exists():
        raise RuntimeError(f"alembic.ini not found at {_ALEMBIC_INI}")
    cfg = Config(str(_ALEMBIC_INI))
    cfg.set_main_option("script_location", str(_MIGRATIONS))
    cfg.set_main_option("sqlalchemy.url", settings.database_url)
    return cfg


def upgrade_head() -> None:
    """Apply all pending migrations."""
    command.upgrade(_config(), "head")


def downgrade(revision: str = "-1") -> None:
    command.downgrade(_config(), revision)


def make_revision(message: str) -> None:
    """Autogenerate a new migration from model changes."""
    command.revision(_config(), message=message, autogenerate=True)
