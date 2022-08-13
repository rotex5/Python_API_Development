"""add content column to posts table

Revision ID: 497335186774
Revises: d8a9748bdf5e
Create Date: 2022-08-12 15:09:54.916284

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '497335186774'
down_revision = 'd8a9748bdf5e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column('posts', 'content')
    pass
