"""add users

Revision ID: a0484a2ba41a
Revises: 380e193c73f2
Create Date: 2026-04-29 20:28:07.909751

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "a0484a2ba41a"
down_revision: Union[str, Sequence[str], None] = "380e193c73f2"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_table(
        "users",
        sa.Column("id", sa.Integer(), nullable=False),
        sa.Column("user_name", sa.String(length=30), nullable=False),
        sa.Column("age", sa.Integer(), nullable=False),
        sa.Column("location", sa.String(length=100), nullable=False),
        sa.Column("email", sa.String(length=100), nullable=False),
        sa.Column("hashed_pass", sa.String(), nullable=False),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade() -> None:
    op.drop_table("users")
