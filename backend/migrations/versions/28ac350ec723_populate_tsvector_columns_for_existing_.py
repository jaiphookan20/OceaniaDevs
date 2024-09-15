"""Populate tsvector columns for existing data

Revision ID: 28ac350ec723
Revises: c5b647fdd0e0
Create Date: 2024-09-09 11:22:44.590715

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '28ac350ec723'
down_revision = 'c5b647fdd0e0'
branch_labels = None
depends_on = None


def upgrade():
    op.execute("""
    UPDATE jobs
    SET search_vector = 
        setweight(to_tsvector('english', coalesce(title,'')), 'A') ||
        setweight(to_tsvector('english', coalesce(description,'')), 'C');

    UPDATE companies
    SET name_vector = to_tsvector('english', coalesce(name,''));

    UPDATE technologies
    SET name_vector = to_tsvector('english', coalesce(name,''));
    """)


def downgrade():
    op.execute("""
    UPDATE jobs SET search_vector = NULL;
    UPDATE companies SET name_vector = NULL;
    UPDATE technologies SET name_vector = NULL;
    """)
