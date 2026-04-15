"""change hotesl

Revision ID: 380e193c73f2
Revises: e20a1937170d
Create Date: 2026-04-14 21:15:38.095007

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "380e193c73f2"
down_revision: Union[str, Sequence[str], None] = "e20a1937170d"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column(
        "hotels", sa.Column("city", sa.String(length=200), nullable=False)
    )
    op.add_column(
        "hotels", sa.Column("street", sa.String(length=200), nullable=False)
    )
    op.drop_column("hotels", "location")


def downgrade() -> None:
    op.add_column(
        "hotels",
        sa.Column(
            "location",
            sa.VARCHAR(length=200),
            autoincrement=False,
            nullable=False,
        ),
    )
    op.drop_column("hotels", "street")
    op.drop_column("hotels", "city")
