"""add last two columns on posts table

Revision ID: 241783a35055
Revises: 798fcd7ce922
Create Date: 2022-09-26 18:56:59.189815

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '241783a35055'
down_revision = '798fcd7ce922'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column(
        'published', sa.Boolean(), nullable=False, server_default='TRUE'),)
    op.add_column('posts', sa.Column(
        'created_at', sa.TIMESTAMP(timezone=True), nullable=False, server_default=sa.text('NOW()')),)
    pass


def downgrade() -> None:
    op.drop_column('posts', 'published')
    op.drop_column('posts', 'created_at')
    pass
