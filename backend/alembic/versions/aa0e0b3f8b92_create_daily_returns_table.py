"""create daily_returns table

Revision ID: aa0e0b3f8b92
Revises: 05599783f610
Create Date: 2025-08-14 14:57:58.880405

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aa0e0b3f8b92'
down_revision: Union[str, Sequence[str], None] = '05599783f610'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
