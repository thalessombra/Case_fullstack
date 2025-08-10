"""add hashed_password to clients

Revision ID: db872e5aba8d
Revises: c92654f11c1c
Create Date: 2025-08-10 11:43:42.113865

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'db872e5aba8d'
down_revision: Union[str, Sequence[str], None] = '0652168562c3'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    op.add_column('clients', sa.Column('hashed_password', sa.String(length=200), nullable=False))


def downgrade() -> None:
    op.drop_column('clients', 'hashed_password')
