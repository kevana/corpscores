"""Added phone info to User.

Revision ID: 380e15516f2d
Revises: d4b786027fd
Create Date: 2014-06-14 23:12:23.007325

"""

# revision identifiers, used by Alembic.
revision = '380e15516f2d'
down_revision = 'd4b786027fd'

from alembic import op
import sqlalchemy as sa

from dci_notify.user.models import User


def upgrade():
    bind = op.get_bind()
    typ = User.__table__.c.carrier.type
    typ._on_table_create(User.__table__, bind, checkfirst=True)
    op.add_column('users', sa.Column('carrier', sa.Enum('suncom', 'nextel', 'powertel', 'bellsouthmobility', 'sprint', 'telus_mobility', 'virgin', 'comcast', 'southernlink', 'boost', 'pscwireless', 'cricket', 'metropcs', 'tracfone', 'verizon', 'bell_atlantic', 'uscellular', 'qwest', 'kajeet', 't_mobile', 'at&t', 'cellularsouth', 'alltel', 'blueskyfrog', 'ameritech', name='Carriers'), nullable=True))
    op.add_column('users', sa.Column('phone_active', sa.Boolean(), nullable=True))
    op.add_column('users', sa.Column('phone_num', sa.String(length=10), nullable=True))


def downgrade():
    op.drop_column('users', 'phone_num')
    op.drop_column('users', 'phone_active')
    op.drop_column('users', 'carrier')
