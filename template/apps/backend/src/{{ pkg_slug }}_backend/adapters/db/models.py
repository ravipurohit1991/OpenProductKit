"""SQLModel tables. This is persistence detail — it lives in the adapter, never
in the core. The core's Project/Note are plain dataclasses; these are storage."""

from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


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
