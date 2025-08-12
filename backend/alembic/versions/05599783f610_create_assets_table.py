"""create assets table

Revision ID: 05599783f610
Revises: aeabea23432e
Create Date: 2025-08-12 15:42:29.181490

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '05599783f610'
down_revision: Union[str, Sequence[str], None] = 'aeabea23432e'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    """Upgrade schema."""
    pass


def downgrade() -> None:
    """Downgrade schema."""
    pass
