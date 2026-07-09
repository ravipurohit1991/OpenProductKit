# [demo] Resource Vault sample domain — replace with your product's entities (see AGENTS.md).
"""The Project domain entity — a container that groups notes."""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _new_id() -> str:
    return uuid4().hex


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class Project:
    name: str
    id: str = field(default_factory=_new_id)
    created_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.name.strip():
            raise ValueError("Project name must not be empty")
