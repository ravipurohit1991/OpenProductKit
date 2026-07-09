from __future__ import annotations

from dataclasses import dataclass
from enum import StrEnum


class HealthLevel(StrEnum):
    OK = "ok"
    DEGRADED = "degraded"
    ERROR = "error"


@dataclass(frozen=True)
class HealthStatus:
    level: HealthLevel = HealthLevel.OK
    message: str = ""

    @classmethod
    def ok(cls, message: str = "") -> HealthStatus:
        return cls(HealthLevel.OK, message)

    @classmethod
    def degraded(cls, message: str) -> HealthStatus:
        return cls(HealthLevel.DEGRADED, message)

    @classmethod
    def error(cls, message: str) -> HealthStatus:
        return cls(HealthLevel.ERROR, message)
