"""Add hashed_password column to clients

Revision ID: 0903d22ba548
Revises: 6d842e8b16ed
Create Date: 2025-08-11 15:25:19.327282

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '0903d22ba548'
down_revision: Union[str, Sequence[str], None] = '6d842e8b16ed'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
