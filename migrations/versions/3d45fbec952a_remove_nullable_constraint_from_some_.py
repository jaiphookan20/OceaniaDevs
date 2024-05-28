"""Remove nullable constraint from some fields in Seeker

Revision ID: 3d45fbec952a
Revises: c3b518f5b4ef
Create Date: 2024-05-10 20:45:42.329873

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '3d45fbec952a'
down_revision = 'c3b518f5b4ef'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seekers', schema=None) as batch_op:
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=255),
               nullable=True)
        batch_op.alter_column('state',
               existing_type=postgresql.ENUM('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'),
               nullable=True)
        batch_op.alter_column('country',
               existing_type=postgresql.ENUM('Australia', 'New Zealand', name='country_enum'),
               nullable=True)

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('seekers', schema=None) as batch_op:
        batch_op.alter_column('country',
               existing_type=postgresql.ENUM('Australia', 'New Zealand', name='country_enum'),
               nullable=False)
        batch_op.alter_column('state',
               existing_type=postgresql.ENUM('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'),
               nullable=False)
        batch_op.alter_column('city',
               existing_type=sa.VARCHAR(length=255),
               nullable=False)

    # ### end Alembic commands ###