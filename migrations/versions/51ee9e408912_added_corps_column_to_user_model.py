"""Added corps column to User model.

Revision ID: 51ee9e408912
Revises: 380e15516f2d
Create Date: 2014-06-28 01:57:49.229877

"""

# revision identifiers, used by Alembic.
revision = '51ee9e408912'
down_revision = '380e15516f2d'

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

def upgrade():
    op.add_column('users', sa.Column('corps', sa.String(length=80), nullable=True))


def downgrade():
    op.drop_column('users', 'corps')
