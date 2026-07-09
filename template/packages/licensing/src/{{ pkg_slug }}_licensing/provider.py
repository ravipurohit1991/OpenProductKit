from __future__ import annotations

from typing import Protocol, runtime_checkable


@runtime_checkable
class LicenseProvider(Protocol):
    def current_plan(self) -> str:
        """The plan the current installation is licensed for."""
        ...

    def is_entitled(self, required_plan: str | None) -> bool:
        """Whether the current plan satisfies `required_plan` (None = free)."""
        ...
