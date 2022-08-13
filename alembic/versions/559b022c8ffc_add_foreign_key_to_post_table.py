"""add foreign-key to post table

Revision ID: 559b022c8ffc
Revises: 5d9253eb6861
Create Date: 2022-08-12 15:40:23.968752

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '559b022c8ffc'
down_revision = '5d9253eb6861'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('owner_id', sa.Integer(), nullable=False))
    op.create_foreign_key('post_users_fk', source_table="posts", referent_table="users",
            local_cols=['owner_id'], remote_cols=['id'], ondelete="CASCADE")
    pass


def downgrade() -> None:
    op.drop_constraint('post_users_fk', table_name="posts")
    op.drop_column('posts', 'owner_id')
    pass
