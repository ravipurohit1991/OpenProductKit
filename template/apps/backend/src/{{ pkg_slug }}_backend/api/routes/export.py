# [demo] Resource Vault sample domain — but ALSO the license-gating example.
# When you replace it, keep the pattern: `Depends(require_plan(...))` on a route.
"""Vault export — the demo of a license-gated route.

The whole gate is the one `Depends(require_plan("pro"))` line; everything else
is a plain route. Run with `APP_LICENSE_DEV_PLAN=free` to see it locked.
"""

from __future__ import annotations

from datetime import UTC, datetime

from fastapi import APIRouter, Depends
from pydantic import BaseModel

from ...licensing import require_plan
from ..deps import NoteServiceDep, ProjectServiceDep
from .notes import NoteOut
from .notes import _to_out as _note_out
from .projects import ProjectOut
from .projects import _to_out as _project_out

router = APIRouter(prefix="/api/export", tags=["export"])


class ExportOut(BaseModel):
    generated_at: str
    projects: list[ProjectOut]
    notes: list[NoteOut]


@router.get("", response_model=ExportOut, dependencies=[Depends(require_plan("pro"))])
def export_vault(projects: ProjectServiceDep, notes: NoteServiceDep) -> ExportOut:
    return ExportOut(
        generated_at=datetime.now(UTC).isoformat(timespec="seconds"),
        projects=[_project_out(p) for p in projects.list()],
        notes=[_note_out(n) for n in notes.search()],
    )
