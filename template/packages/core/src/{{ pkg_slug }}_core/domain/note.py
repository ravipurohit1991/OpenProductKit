"""The Note domain entity.

Deliberately a plain stdlib dataclass with zero third-party dependencies. The
whole point of this template is that the core knows nothing about HTTP, SQL,
Pydantic or any framework — it is just business rules.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _new_id() -> str:
    return uuid4().hex


def _now() -> datetime:
    return datetime.now(UTC)


@dataclass(frozen=True, slots=True)
class Note:
    title: str
    body: str = ""
    id: str = field(default_factory=_new_id)
    created_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Note title must not be empty")
