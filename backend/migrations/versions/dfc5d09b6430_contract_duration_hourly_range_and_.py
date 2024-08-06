"""contract_duration, hourly_range, and daily_range fields to Job model

Revision ID: dfc5d09b6430
Revises: 
Create Date: 2024-08-04 05:33:35.311095

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'dfc5d09b6430'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.add_column(sa.Column('hourly_range', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('daily_range', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.drop_column('daily_range')
        batch_op.drop_column('hourly_range')

    # ### end Alembic commands ###