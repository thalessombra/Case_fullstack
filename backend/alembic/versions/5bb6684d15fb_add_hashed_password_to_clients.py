"""Add hashed_password to clients

Revision ID: 5bb6684d15fb
Revises: 0903d22ba548
Create Date: 2025-08-12 12:19:09.777992

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '5bb6684d15fb'
down_revision: Union[str, Sequence[str], None] = '0903d22ba548'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.add_column('clients', sa.Column('hashed_password', sa.String(), nullable=False))


def downgrade():
    op.drop_column('clients', 'hashed_password')
