from __future__ import annotations

from dataclasses import dataclass, field, replace
from datetime import UTC, datetime
from enum import StrEnum
from uuid import uuid4


def utcnow() -> datetime:
    return datetime.now(UTC).replace(tzinfo=None)


class JobStatus(StrEnum):
    QUEUED = "queued"
    RUNNING = "running"
    SUCCEEDED = "succeeded"
    FAILED = "failed"
    CANCELLED = "cancelled"


class ProviderResultStatus(StrEnum):
    PENDING = "pending"
    SUCCEEDED = "succeeded"
    FAILED = "failed"


@dataclass(frozen=True, slots=True)
class GenerationRequest:
    job_id: str
    prompt: str
    model: str
    input_url: str | None
    callback_url: str


@dataclass(frozen=True, slots=True)
class ProviderResult:
    status: ProviderResultStatus
    request_id: str = ""
    output_url: str | None = None
    error: str | None = None


@dataclass(frozen=True, slots=True)
class GenerationJob:
    owner_id: str
    prompt: str
    model: str
    provider: str
    cost_credits: int
    client_request_id: str
    id: str = field(default_factory=lambda: uuid4().hex)
    status: JobStatus = JobStatus.QUEUED
    input_asset_id: str | None = None
    output_url: str | None = None
    provider_request_id: str | None = None
    error: str | None = None
    created_at: datetime = field(default_factory=utcnow)
    updated_at: datetime = field(default_factory=utcnow)

    def __post_init__(self) -> None:
        if not self.owner_id:
            raise ValueError("Generation job must have an owner")
        if not self.prompt.strip():
            raise ValueError("Prompt must not be empty")
        if self.cost_credits < 1:
            raise ValueError("Credit cost must be positive")

    def with_status(self, status: JobStatus, **changes: object) -> GenerationJob:
        return replace(self, status=status, updated_at=utcnow(), **changes)
