"""Add tsvector columns on Company.name and Technology.name for full-text search

Revision ID: c5b647fdd0e0
Revises: 9397f595769f
Create Date: 2024-09-09 10:15:38.176599

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'c5b647fdd0e0'
down_revision = '9397f595769f'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_vector', postgresql.TSVECTOR(), nullable=True))

    with op.batch_alter_table('technologies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('name_vector', postgresql.TSVECTOR(), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('technologies', schema=None) as batch_op:
        batch_op.drop_column('name_vector')

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_column('name_vector')

    # ### end Alembic commands ###
