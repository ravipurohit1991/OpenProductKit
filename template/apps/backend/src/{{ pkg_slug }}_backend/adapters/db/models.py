"""SQLModel tables. This is persistence detail — it lives in the adapter, never
in the core. The core's Note is a plain dataclass; NoteRow is how we store it."""

from __future__ import annotations

from datetime import datetime

from sqlmodel import Field, SQLModel


class NoteRow(SQLModel, table=True):
    __tablename__ = "notes"

    id: str = Field(primary_key=True)
    title: str
    body: str = ""
    created_at: datetime
