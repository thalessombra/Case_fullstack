"""Remove role and created_at from clients

Revision ID: aeabea23432e
Revises: 42cd4744cacd
Create Date: 2025-08-12 14:38:53.708421

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'aeabea23432e'
down_revision: Union[str, Sequence[str], None] = '42cd4744cacd'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('clients', 'role')
    op.drop_column('clients', 'created_at')

def downgrade():
    op.add_column('clients', sa.Column('role', sa.String(), nullable=True))
    op.add_column('clients', sa.Column('created_at', sa.DateTime(), nullable=True))