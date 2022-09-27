"""create post table

Revision ID: 263e4d25401f
Revises: 
Create Date: 2022-09-26 16:29:55.097644

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '263e4d25401f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade() -> None:
    op.create_table('posts', sa.Column('id', sa.Integer(), nullable=False, primary_key=True), sa.Column('title', sa.String(), nullable=False))
    pass


def downgrade() -> None:
    op.drop_table('posts')
    pass
