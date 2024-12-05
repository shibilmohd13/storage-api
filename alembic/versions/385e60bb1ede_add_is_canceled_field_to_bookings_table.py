"""Add is_canceled field to bookings table

Revision ID: 385e60bb1ede
Revises: e4326a7c7f3e
Create Date: 2024-12-05 10:16:24.013638

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '385e60bb1ede'
down_revision = 'e4326a7c7f3e'
branch_labels = None
depends_on = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.add_column('bookings', sa.Column('is_canceled', sa.Boolean(), nullable=True))
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_column('bookings', 'is_canceled')
    # ### end Alembic commands ###
