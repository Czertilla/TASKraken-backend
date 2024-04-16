"""set folders nullable

Revision ID: 1775dbf6761b
Revises: 97265783872a
Create Date: 2024-04-14 22:36:22.960380

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '1775dbf6761b'
down_revision: Union[str, None] = '97265783872a'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('reports', 'folder_id',
               existing_type=sa.UUID(),
               nullable=True)
    op.create_foreign_key("structures_head_id_fkey", 'structures', 'roles', ['head_id'], ['id'])
    op.add_column('tasks', sa.Column('folder_id', sa.Uuid(), nullable=True))
    op.create_foreign_key("tasks_folder_id_fkey", 'tasks', 'folders', ['folder_id'], ['id'])
    op.alter_column('user', 'photo_folder_id',
               existing_type=sa.UUID(),
               nullable=True)
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.alter_column('user', 'photo_folder_id',
               existing_type=sa.UUID(),
               nullable=False)
    op.drop_constraint("tasks_folder_id_fkey", 'tasks', type_='foreignkey')
    op.drop_column('tasks', 'folder_id')
    op.drop_constraint("structures_head_id_fkey", 'structures', type_='foreignkey')
    op.alter_column('reports', 'folder_id',
               existing_type=sa.UUID(),
               nullable=False)
    # ### end Alembic commands ###
