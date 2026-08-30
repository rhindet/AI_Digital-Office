"""add created_by to tickets

Revision ID: 1e83a7c9ed73
Revises: 
Create Date: 2026-08-24 21:57:37.432035

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1e83a7c9ed73'
down_revision: Union[str, Sequence[str], None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "tickets",
        sa.Column(
            "created_by",
            sa.Integer(),
            nullable=True,
        ),
    )

    op.execute(
        """
        UPDATE tickets
        SET created_by = (
            SELECT id
            FROM users
            ORDER BY id
            LIMIT 1
        )
        WHERE created_by IS NULL
        """
    )

    op.alter_column(
        "tickets",
        "created_by",
        existing_type=sa.Integer(),
        nullable=False,
    )

    op.create_foreign_key(
        "fk_tickets_created_by_users",
        "tickets",
        "users",
        ["created_by"],
        ["id"],
    )


def downgrade() -> None:
    op.drop_constraint(
        "fk_tickets_created_by_users",
        "tickets",
        type_="foreignkey",
    )

    op.drop_column(
        "tickets",
        "created_by",
    )
