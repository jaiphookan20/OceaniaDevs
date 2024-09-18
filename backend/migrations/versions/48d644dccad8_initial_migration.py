"""initial migration

Revision ID: 48d644dccad8
Revises: 28ac350ec723
Create Date: 2024-09-12 14:00:06.872828

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '48d644dccad8'
down_revision = '28ac350ec723'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.drop_index('companies_name_trgm_idx', postgresql_using='gin')

    with op.batch_alter_table('technologies', schema=None) as batch_op:
        batch_op.create_index('technologies_name_trgm_idx', ['name'], unique=False, postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('technologies', schema=None) as batch_op:
        batch_op.drop_index('technologies_name_trgm_idx', postgresql_using='gin', postgresql_ops={'name': 'gin_trgm_ops'})

    with op.batch_alter_table('companies', schema=None) as batch_op:
        batch_op.create_index('companies_name_trgm_idx', ['name'], unique=False, postgresql_using='gin')

    # ### end Alembic commands ###
