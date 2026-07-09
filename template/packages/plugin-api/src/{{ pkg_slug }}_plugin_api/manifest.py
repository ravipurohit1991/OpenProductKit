from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class PluginManifest:
    """Declarative metadata a plugin advertises about itself."""

    id: str
    name: str
    version: str = "0.1.0"
    author: str = ""
    description: str = ""
    #: Declared permissions, e.g. "network:none", "filesystem:read". Displayed
    #: to the operator; enforcement is a roadmap item.
    permissions: tuple[str, ...] = ()
    #: Plan required to run this plugin, or None if free. Checked by the license
    #: provider (see the licensing package).
    required_plan: str | None = None
