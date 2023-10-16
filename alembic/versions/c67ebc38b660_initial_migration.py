"""initial migration

Revision ID: c67ebc38b660
Revises: 
Create Date: 2023-10-13 23:22:00.158944

"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = 'c67ebc38b660'
down_revision = None
branch_labels = None
depends_on = None

def upgrade() -> None:
    op.create_table(
        'addresses',
        sa.Column('id', sa.Integer, primary_key=True, index=True),
        sa.Column('name', sa.String(255)),
        sa.Column('latitude', sa.String(20)),
        sa.Column('longitude', sa.String(255)),
    )

def downgrade() -> None:
    op.drop_table('addresses')
