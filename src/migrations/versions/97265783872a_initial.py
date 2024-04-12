"""initial

Revision ID: 97265783872a
Revises: 
Create Date: 2024-04-12 15:09:16.356615

"""
from typing import Sequence, Union

from alembic import op
import fastapi_users_db_sqlalchemy
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '97265783872a'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None

taskstatus = sa.Enum('created', 'frozen', 'resumed', 'closed', 'completed', name='taskstatus')

def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('folders',
        sa.Column('head_folder_id', sa.Uuid(), nullable=True),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['head_folder_id'], ['folders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('structures',
        sa.Column('head_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('desctription', sa.String(), nullable=False, default=""),
        sa.Column('enclosure_id', sa.Uuid(), nullable=True),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['enclosure_id'], ['structures.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    
    op.create_table('user',
        sa.Column('username', sa.String(), nullable=False),
        sa.Column('photo_folder_id', sa.Uuid(), nullable=False),
        sa.Column('id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=False),
        sa.Column('email', sa.String(length=320), nullable=False),
        sa.Column('hashed_password', sa.String(length=1024), nullable=False),
        sa.Column('is_active', sa.Boolean(), nullable=False),
        sa.Column('is_superuser', sa.Boolean(), nullable=False),
        sa.Column('is_verified', sa.Boolean(), nullable=False),
        sa.ForeignKeyConstraint(['photo_folder_id'], ['folders.id'], ),
        sa.PrimaryKeyConstraint('id'),
        sa.UniqueConstraint('username')
    )

    op.create_table('roles',
        sa.Column('user_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('structure_id', sa.Uuid(), nullable=False),
        sa.Column('chief_id', fastapi_users_db_sqlalchemy.generics.GUID(), nullable=True),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['chief_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['structure_id'], ['structures.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['user.id'], ondelete='SET NULL'),
        sa.PrimaryKeyConstraint('id')
    )

    op.batch_alter_table('structures',
        sa.ForeignKeyConstraint(['head_id'], ['roles.id']),
    )

    op.create_table('files',
        sa.Column('data', sa.LargeBinary(), nullable=True),
        sa.Column('name', sa.String(), nullable=True),
        sa.Column('folder_id', sa.Uuid(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('changed_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['folder_id'], ['folders.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_table('projects',
        sa.Column('organization_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('desctription', sa.String(), nullable=False, default=""),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('creator_id', sa.Uuid(), nullable=False),
        sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', sa.Enum('created', 'frozen', 'resumed', 'closed', 'completed', name='taskstatus'), nullable=False),
        sa.Column('status_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['organization_id'], ['structures.id'], ),
        sa.PrimaryKeyConstraint('id')
    )

    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)

    op.create_table('tasks',
        sa.Column('level', sa.Integer(), nullable=False),
        sa.Column('project_id', sa.Uuid(), nullable=False),
        sa.Column('head_task_id', sa.Uuid(), nullable=True),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('desctription', sa.String(), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), nullable=False),
        sa.Column('creator_id', sa.Uuid(), nullable=False),
        sa.Column('edited_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('deadline', sa.DateTime(timezone=True), nullable=True),
        sa.Column('status', taskstatus, nullable=False),
        sa.Column('status_timestamp', sa.DateTime(timezone=True), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['creator_id'], ['roles.id'], ),
        sa.ForeignKeyConstraint(['head_task_id'], ['tasks.id'], ),
        sa.ForeignKeyConstraint(['project_id'], ['projects.id'], ),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('checklists',
        sa.Column('task_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    op.create_table('reports',
        sa.Column('task_id', sa.Uuid(), nullable=False),
        sa.Column('responsible_id', sa.Uuid(), nullable=False),
        sa.Column('folder_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['folder_id'], ['folders.id'], ),
        sa.ForeignKeyConstraint(['responsible_id'], ['roles.id'], ondelete='SET NULL'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'id')
    )
    op.create_table('responsibilities',
        sa.Column('task_id', sa.Uuid(), nullable=False),
        sa.Column('role_id', sa.Uuid(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['role_id'], ['roles.id'], ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['task_id'], ['tasks.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('task_id', 'role_id', 'id')
    )
    op.create_table('checkpoints',
        sa.Column('checklist_id', sa.Uuid(), nullable=False),
        sa.Column('name', sa.String(), nullable=False),
        sa.Column('done', sa.Boolean(), nullable=False),
        sa.Column('id', sa.Uuid(), nullable=False),
        sa.ForeignKeyConstraint(['checklist_id'], ['checklists.id'], ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('checkpoints')
    op.drop_table('responsibilities')
    op.drop_table('reports')
    op.drop_table('checklists')
    op.drop_table('tasks')
    op.drop_table('projects')
    op.drop_table('files')
    op.drop_column('structures', "head_id")
    op.drop_table('roles')
    op.drop_table('structures')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_table('folders')
    taskstatus.drop(op.get_bind(), checkfirst=False)
    # ### end Alembic commands ###
