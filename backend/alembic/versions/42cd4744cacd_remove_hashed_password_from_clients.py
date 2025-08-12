"""Remove hashed_password from clients

Revision ID: 42cd4744cacd
Revises: 5bb6684d15fb
Create Date: 2025-08-12 12:38:50.362991

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = '42cd4744cacd'
down_revision: Union[str, Sequence[str], None] = '5bb6684d15fb'
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade():
    op.drop_column('clients', 'hashed_password')

def downgrade():
    op.add_column('clients', sa.Column('hashed_password', sa.String(), nullable=False))
