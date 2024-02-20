"""add grade_date row

Revision ID: 3bddfbc04507
Revises: e66a0065ad1e
Create Date: 2024-02-19 23:22:00.247538

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '3bddfbc04507'
down_revision: Union[str, None] = 'e66a0065ad1e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('grades', sa.Column('grade_date', sa.Date(), nullable=False))


def downgrade() -> None:
    op.drop_column('grades', 'grade_date')
