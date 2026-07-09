"""Persistence for plugin enable/disable state."""

from __future__ import annotations

from sqlmodel import Session, select

from .models import PluginStateRow


def get_enabled_map(session: Session) -> dict[str, bool]:
    rows = session.exec(select(PluginStateRow)).all()
    return {row.plugin_id: row.enabled for row in rows}


def set_enabled(session: Session, plugin_id: str, enabled: bool) -> None:
    row = session.get(PluginStateRow, plugin_id)
    if row is None:
        row = PluginStateRow(plugin_id=plugin_id, enabled=enabled)
    else:
        row.enabled = enabled
    session.add(row)
    session.commit()
