from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class NavItem:
    """A navigation entry a plugin contributes to the admin UI."""

    label: str
    path: str
    icon: str = ""
