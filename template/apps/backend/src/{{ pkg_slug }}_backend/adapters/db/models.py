"""SQLModel tables. This is persistence detail — it lives in the adapter, never
in the core. The core's Project/Note are plain dataclasses; these are storage."""

from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel

# [demo] ProjectRow/NoteRow/NoteTagRow are the Resource Vault sample tables —
# replace them with your own. PluginStateRow below is framework: keep it.


class ProjectRow(SQLModel, table=True):
    __tablename__ = "projects"

    id: str = Field(primary_key=True)
    name: str
    created_at: datetime


class NoteRow(SQLModel, table=True):
    __tablename__ = "notes"

    id: str = Field(primary_key=True)
    project_id: str = Field(foreign_key="projects.id", index=True)
    title: str
    body: str = ""
    created_at: datetime


class NoteTagRow(SQLModel, table=True):
    __tablename__ = "note_tags"

    note_id: str = Field(foreign_key="notes.id", primary_key=True)
    tag: str = Field(primary_key=True, index=True)


class PluginStateRow(SQLModel, table=True):
    """Persisted enable/disable state for a discovered plugin."""

    __tablename__ = "plugin_states"

    plugin_id: str = Field(primary_key=True)
    enabled: bool = Field(default=True)


class UserRow(SQLModel, table=True):
    """A user account. Only consulted when APP_AUTH_ENABLED is on (hosted
    deployments); the desktop/local story runs without accounts."""

    __tablename__ = "users"

    id: str = Field(primary_key=True)
    email: str = Field(unique=True, index=True)
    password_hash: str
    is_admin: bool = Field(default=False)
    created_at: datetime


class AuthSessionRow(SQLModel, table=True):
    """A bearer session. Only the SHA-256 of the token is stored, so a leaked
    database does not leak usable tokens."""

    __tablename__ = "auth_sessions"

    token_hash: str = Field(primary_key=True)
    user_id: str = Field(foreign_key="users.id", index=True)
    created_at: datetime
    expires_at: datetime
