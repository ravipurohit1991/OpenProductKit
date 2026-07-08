"""initial schema: projects, notes, note_tags

Revision ID: 0001
Revises:
Create Date: 2026-01-01 00:00:00

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "0001"
down_revision: str | None = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "projects",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("name", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_table(
        "notes",
        sa.Column("id", sa.String(), nullable=False),
        sa.Column("project_id", sa.String(), nullable=False),
        sa.Column("title", sa.String(), nullable=False),
        sa.Column("body", sa.String(), nullable=False),
        sa.Column("created_at", sa.DateTime(), nullable=False),
        sa.ForeignKeyConstraint(["project_id"], ["projects.id"]),
        sa.PrimaryKeyConstraint("id"),
    )
    op.create_index("ix_notes_project_id", "notes", ["project_id"])
    op.create_table(
        "note_tags",
        sa.Column("note_id", sa.String(), nullable=False),
        sa.Column("tag", sa.String(), nullable=False),
        sa.ForeignKeyConstraint(["note_id"], ["notes.id"]),
        sa.PrimaryKeyConstraint("note_id", "tag"),
    )
    op.create_index("ix_note_tags_tag", "note_tags", ["tag"])


def downgrade() -> None:
    op.drop_index("ix_note_tags_tag", "note_tags")
    op.drop_table("note_tags")
    op.drop_index("ix_notes_project_id", "notes")
    op.drop_table("notes")
    op.drop_table("projects")
