"""Add new indexes and update search vector

Revision ID: b78cc3f22723
Revises: 0392a427ab90
Create Date: 2024-09-15 10:21:56.079301

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'b78cc3f22723'
down_revision = '0392a427ab90'
branch_labels = None
depends_on = None



def upgrade():
    # Create new indexes
    op.create_index('jobs_specialization_idx', 'jobs', ['specialization'], unique=False)
    op.create_index('jobs_experience_level_idx', 'jobs', ['experience_level'], unique=False)
    op.create_index('jobs_work_location_idx', 'jobs', ['work_location'], unique=False)
    op.create_index('jobs_city_idx', 'jobs', ['city'], unique=False)
    op.create_index('job_technologies_job_id_idx', 'job_technologies', ['job_id'], unique=False)
    op.create_index('job_technologies_technology_id_idx', 'job_technologies', ['technology_id'], unique=False)

    # Update search_vector for existing jobs
    op.execute("""
    UPDATE jobs j
    SET search_vector = subquery.new_search_vector
    FROM (
        SELECT j.job_id,
               setweight(to_tsvector('english', coalesce(j.title,'')), 'A') ||
               setweight(to_tsvector('english', coalesce(j.description,'')), 'B') ||
               setweight(to_tsvector('english', coalesce(j.overview,'')), 'B') ||
               setweight(to_tsvector('english', coalesce(j.responsibilities,'')), 'B') ||
               setweight(to_tsvector('english', coalesce(j.requirements,'')), 'B') ||
               setweight(to_tsvector('english', coalesce(c.name,'')), 'C') ||
               setweight(to_tsvector('english', coalesce(c.description,'')), 'D') AS new_search_vector
        FROM jobs j
        JOIN companies c ON j.company_id = c.company_id
    ) AS subquery
    WHERE j.job_id = subquery.job_id;
    """)

def downgrade():
    # Remove the new indexes
    op.drop_index('jobs_specialization_idx', table_name='jobs')
    op.drop_index('jobs_experience_level_idx', table_name='jobs')
    op.drop_index('jobs_work_location_idx', table_name='jobs')
    op.drop_index('jobs_city_idx', table_name='jobs')
    op.drop_index('job_technologies_job_id_idx', table_name='job_technologies')
    op.drop_index('job_technologies_technology_id_idx', table_name='job_technologies')

    # Reset search_vector to NULL
    op.execute("UPDATE jobs SET search_vector = NULL;")
