"""add content column to post table

Revision ID: 22828312bc7f
Revises: 263e4d25401f
Create Date: 2022-09-26 16:40:25.459234

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '22828312bc7f'
down_revision = '263e4d25401f'
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.add_column('posts', sa.Column('content', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_column
    pass
