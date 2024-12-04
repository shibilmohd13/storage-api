"""Add location column to vault table with default value

Revision ID: e4326a7c7f3e
Revises: 99b732f1f047
Create Date: 2024-12-04 12:35:20.153285

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e4326a7c7f3e'
down_revision = '99b732f1f047'
branch_labels = None
depends_on = None


def upgrade():
    # Add the `location` column with a default value
    op.add_column('vaults', sa.Column('location', sa.String(length=255), nullable=False, server_default='Trivandrum'))

def downgrade():
    # Remove the `location` column
    op.drop_column('vaults', 'location')
