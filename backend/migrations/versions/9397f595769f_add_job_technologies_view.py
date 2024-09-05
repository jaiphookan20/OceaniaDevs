"""add job_technologies_view

Revision ID: 9397f595769f
Revises: 
Create Date: 2024-09-04 02:52:49.079406

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9397f595769f'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### Add the view ###
    op.execute("""
    CREATE OR REPLACE VIEW job_technologies_view AS
    SELECT 
        j.job_id,
        j.title,
        string_agg(t.name, ', ' ORDER BY t.name) AS technologies
    FROM 
        jobs j
    LEFT JOIN 
        job_technologies jt ON j.job_id = jt.job_id
    LEFT JOIN 
        technologies t ON jt.technology_id = t.id
    GROUP BY 
        j.job_id, j.title;
    """)


def downgrade():
     # ### Drop the view ###
    op.execute("DROP VIEW IF EXISTS job_technologies_view;")
