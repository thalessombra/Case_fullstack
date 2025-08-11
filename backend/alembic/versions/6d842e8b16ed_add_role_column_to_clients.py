"""Add role column to clients

Revision ID: 6d842e8b16ed
Revises: ebfc9d72ecd7
Create Date: 2025-08-11 15:11:15.888077

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '6d842e8b16ed'
down_revision: Union[str, Sequence[str], None] = 'ebfc9d72ecd7'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
