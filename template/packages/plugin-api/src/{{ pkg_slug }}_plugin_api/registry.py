"""Discovery and filtering of installed plugins."""

from __future__ import annotations

import importlib.metadata
from collections.abc import Callable, Iterable
from dataclasses import dataclass

from .manifest import PluginManifest
from .plugin import Plugin


def discover(group: str) -> list[Plugin]:
    """Load every plugin advertised under the given entry-point group.

    An entry point may point at a `Plugin` instance or a `Plugin` subclass; a
    class is instantiated with no arguments.
    """
    plugins: list[Plugin] = []
    for entry_point in importlib.metadata.entry_points(group=group):
        obj = entry_point.load()
        plugin = obj() if isinstance(obj, type) else obj
        plugins.append(plugin)
    return sorted(plugins, key=lambda p: p.manifest.id)


@dataclass(frozen=True)
class PluginView:
    """A plugin paired with its resolved enabled/entitled state."""

    plugin: Plugin
    enabled: bool
    entitled: bool

    @property
    def manifest(self) -> PluginManifest:
        return self.plugin.manifest

    @property
    def active(self) -> bool:
        """A plugin runs only if it is both enabled and licensed."""
        return self.enabled and self.entitled


class PluginRegistry:
    def __init__(
        self,
        plugins: Iterable[Plugin],
        is_enabled: Callable[[str], bool],
        is_entitled: Callable[[PluginManifest], bool],
    ) -> None:
        self._views = [
            PluginView(
                plugin=p,
                enabled=is_enabled(p.manifest.id),
                entitled=is_entitled(p.manifest),
            )
            for p in plugins
        ]

    def all(self) -> list[PluginView]:
        return list(self._views)

    def active(self) -> list[PluginView]:
        return [v for v in self._views if v.active]

    def get(self, plugin_id: str) -> PluginView | None:
        return next((v for v in self._views if v.manifest.id == plugin_id), None)
