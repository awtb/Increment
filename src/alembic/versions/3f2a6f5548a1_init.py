"""Init.

Revision ID: 3f2a6f5548a1
Revises:
Create Date: 2025-04-05 15:14:35.515574

"""

from typing import Sequence, Union

import sqlalchemy as sa

from alembic import op

# revision identifiers, used by Alembic.
revision: str = "3f2a6f5548a1"
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table(
        "increment",
        sa.Column("count", sa.Integer(), nullable=False),
        sa.PrimaryKeyConstraint("count"),
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    """Downgrade schema."""
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table("increment")
    # ### end Alembic commands ###
