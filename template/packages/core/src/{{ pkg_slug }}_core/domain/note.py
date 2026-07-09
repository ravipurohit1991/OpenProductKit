# [demo] Resource Vault sample domain — replace with your product's entities (see AGENTS.md).
"""The Note domain entity.

Deliberately a plain stdlib dataclass with zero third-party dependencies. The
whole point of this template is that the core knows nothing about HTTP, SQL,
Pydantic or any framework — it is just business rules.

A note belongs to a project and carries a set of normalized tags.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from datetime import UTC, datetime
from uuid import uuid4


def _new_id() -> str:
    return uuid4().hex


def _now() -> datetime:
    return datetime.now(UTC)


def normalize_tags(tags: object) -> tuple[str, ...]:
    """Lower-case, strip, drop blanks and duplicates while preserving order."""
    if tags is None:
        return ()
    seen: dict[str, None] = {}
    for raw in tags:
        tag = str(raw).strip().lower()
        if tag:
            seen.setdefault(tag, None)
    return tuple(seen)


@dataclass(frozen=True, slots=True)
class Note:
    project_id: str
    title: str
    body: str = ""
    tags: tuple[str, ...] = ()
    id: str = field(default_factory=_new_id)
    created_at: datetime = field(default_factory=_now)

    def __post_init__(self) -> None:
        if not self.title.strip():
            raise ValueError("Note title must not be empty")
        if not self.project_id:
            raise ValueError("Note must belong to a project")
        # Enforce normalized tags even when constructed directly.
        object.__setattr__(self, "tags", normalize_tags(self.tags))

    def matches(self, query: str) -> bool:
        """True if the free-text query occurs in the title, body or a tag."""
        q = query.strip().lower()
        if not q:
            return True
        return (
            q in self.title.lower()
            or q in self.body.lower()
            or any(q in tag for tag in self.tags)
        )
