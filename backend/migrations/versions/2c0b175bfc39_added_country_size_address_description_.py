"""Added country, size, address, description, logo_url to Company model

Revision ID: 2c0b175bfc39
Revises: 6f89c69db19e
Create Date: 2024-06-23 00:49:05.469742

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '2c0b175bfc39'
down_revision = '6f89c69db19e'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.add_column(sa.Column('country', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('size', sa.String(length=100), nullable=True))
        batch_op.add_column(sa.Column('address', sa.String(length=255), nullable=True))
        batch_op.add_column(sa.Column('description', sa.Text(), nullable=True))
        batch_op.add_column(sa.Column('logo_url', sa.String(length=255), nullable=True))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_column('logo_url')
        batch_op.drop_column('description')
        batch_op.drop_column('address')
        batch_op.drop_column('size')
        batch_op.drop_column('country')

    # ### end Alembic commands ###