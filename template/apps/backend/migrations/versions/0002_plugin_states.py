"""plugin enable/disable state

Revision ID: 0002
Revises: 0001
Create Date: 2026-01-01 00:00:01

"""

from __future__ import annotations

import sqlalchemy as sa
from alembic import op

revision: str = "0002"
down_revision: str | None = "0001"
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table(
        "plugin_states",
        sa.Column("plugin_id", sa.String(), nullable=False),
        sa.Column("enabled", sa.Boolean(), nullable=False),
        sa.PrimaryKeyConstraint("plugin_id"),
    )


def downgrade() -> None:
    op.drop_table("plugin_states")
