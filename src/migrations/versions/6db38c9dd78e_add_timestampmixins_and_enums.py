"""add timestampMixins and Enums

Revision ID: 6db38c9dd78e
Revises: 7981f7f2c698
Create Date: 2024-04-16 17:57:59.731219

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

from models.roles import RoleORM
from models.structures import StructureORM

# revision identifiers, used by Alembic.
revision: str = '6db38c9dd78e'
down_revision: Union[str, None] = '7981f7f2c698'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('files', sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True))
    op.drop_column('files', 'changed_at')

    op.add_column('roles', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('roles', sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True))
    op.execute(sa.update(RoleORM).where(RoleORM.created_at==None).values(created_at=sa.func.now()))
    op.alter_column("roles", "created_at", nullable=False)


    op.add_column('structures', sa.Column('created_at', sa.DateTime(timezone=True), nullable=True))
    op.add_column('structures', sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True))
    op.execute(sa.update(StructureORM).where(StructureORM.created_at==None).values(created_at=sa.func.now()))
    op.alter_column("structures", "created_at", nullable=False)

    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('structures', 'edited_at')
    op.drop_column('structures', 'created_at')
    op.drop_column('roles', 'edited_at')
    op.drop_column('roles', 'created_at')
    op.add_column('files', sa.Column('changed_at', postgresql.TIMESTAMP(timezone=True), autoincrement=False, nullable=True))
    op.drop_column('files', 'edited_at')
    # ### end Alembic commands ###
