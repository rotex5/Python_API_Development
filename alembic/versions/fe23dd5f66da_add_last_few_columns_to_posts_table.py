"""add last few columns to posts table

Revision ID: fe23dd5f66da
Revises: 559b022c8ffc
Create Date: 2022-08-12 16:15:52.489777

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fe23dd5f66da'
down_revision = '559b022c8ffc'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
            'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
            'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text
            ('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
