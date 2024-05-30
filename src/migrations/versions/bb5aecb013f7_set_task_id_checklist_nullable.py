"""set task_id checklist nullable

Revision ID: bb5aecb013f7
Revises: 96201eea6c2d
Create Date: 2024-05-30 19:43:37.899708

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'bb5aecb013f7'
down_revision: Union[str, None] = '96201eea6c2d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('checklists', 'task_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('checklists', 'task_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
