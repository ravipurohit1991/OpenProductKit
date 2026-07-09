from __future__ import annotations

from dataclasses import dataclass, field
from datetime import datetime
from typing import Protocol, runtime_checkable


@dataclass(frozen=True)
class LicenseInfo:
    """Everything an adapter (API route, CLI, UI) may want to show about a license."""

    plan: str = "free"
    licensee: str = ""
    features: tuple[str, ...] = field(default=())
    expires_at: datetime | None = None
    valid: bool = False
    #: Where the entitlement came from: none | dev | token | file | http.
    source: str = "none"
    #: Human-readable status, e.g. why validation failed or that it is stale.
    message: str = ""


@runtime_checkable
class LicenseProvider(Protocol):
    def current_plan(self) -> str:
        """The plan the current installation is licensed for."""
        ...

    def is_entitled(self, required_plan: str | None) -> bool:
        """Whether the current plan satisfies `required_plan` (None = free)."""
        ...

    def has_feature(self, feature: str) -> bool:
        """Whether the license explicitly grants a named feature flag."""
        ...

    def info(self) -> LicenseInfo:
        """Full license details for display (plan, licensee, expiry, source)."""
        ...
