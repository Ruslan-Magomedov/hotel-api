"""make email unique

Revision ID: 0c2344088bdc
Revises: eb4c0da45529
Create Date: 2026-05-01 14:51:23.522158

"""

from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision: str = "0c2344088bdc"
down_revision: Union[str, Sequence[str], None] = "eb4c0da45529"
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.create_unique_constraint(None, "users", ["email"])


def downgrade() -> None:
    op.drop_constraint(None, "users", type_="unique")
