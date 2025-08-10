"""Add hashed_password column to clients

Revision ID: ebfc9d72ecd7
Revises: db872e5aba8d
Create Date: 2025-08-10 13:34:50.537527

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'ebfc9d72ecd7'
down_revision: Union[str, Sequence[str], None] = 'db872e5aba8d'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
