from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '1c7d58b5de1d'
down_revision = 'ee8f1cfd0653'
branch_labels = None
depends_on = None

def upgrade():
    # Define ENUM types with all necessary values
    specialization_enum = postgresql.ENUM(
        'Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing',
        'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity',
        name='specialization_enum'
    )
    specialization_enum.create(op.get_bind())

    work_location_enum = postgresql.ENUM(
        'Remote', 'Hybrid', 'Office', name='work_location_enum'
    )
    work_location_enum.create(op.get_bind())

    experience_level_enum = postgresql.ENUM(
        'Junior', 'Mid-Level', 'Senior', 'Executive', name='experience_level_enum'
    )
    experience_level_enum.create(op.get_bind())

    job_arrangement_enum = postgresql.ENUM(
        'Permanent', 'Contract/Temp', 'Internship', 'Part-Time', name='job_arrangement_enum'
    )
    job_arrangement_enum.create(op.get_bind())

    # Update existing data to conform to new ENUM values
    # Specialization updates
    op.execute("UPDATE jobs SET specialization = 'Frontend' WHERE specialization = 'Business Application Development'")
    op.execute("UPDATE jobs SET specialization = 'Backend' WHERE specialization = 'DevOps & IT'")
    op.execute("UPDATE jobs SET specialization = 'Cloud & Infra' WHERE specialization = 'Cloud & Infrastructure'")
    op.execute("UPDATE jobs SET specialization = 'Data & ML' WHERE specialization IN ('Machine Learning & AI', 'Business Intelligence & Data')")
    op.execute("UPDATE jobs SET specialization = 'Cybersecurity' WHERE specialization = 'Cybersecurity'")
    op.execute("UPDATE jobs SET specialization = 'QA & Testing' WHERE specialization = 'QA & Testing'")
    op.execute("UPDATE jobs SET specialization = 'Project Management' WHERE specialization = 'Project Management'")
    op.execute("UPDATE jobs SET specialization = 'Full-Stack' WHERE specialization IN ('Full Stack', 'ML & AI', 'Cyber Security')")
    op.execute("UPDATE jobs SET specialization = 'Full-Stack' WHERE specialization NOT IN ('Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity')")

    # Experience level updates
    op.execute("UPDATE jobs SET experience_level = 'Junior' WHERE experience_level = 'Entry Level'")
    op.execute("UPDATE jobs SET experience_level = 'Mid-Level' WHERE experience_level = 'Associate'")
    op.execute("UPDATE jobs SET experience_level = 'Senior' WHERE experience_level = 'Mid-Senior Level'")
    op.execute("UPDATE jobs SET experience_level = 'Senior' WHERE experience_level = 'Director'")
    op.execute("UPDATE jobs SET experience_level = 'Executive' WHERE experience_level = 'Executive'")
    # General update for any experience_level not matching new ENUMs
    op.execute("UPDATE jobs SET experience_level = 'Mid-Level' WHERE experience_level NOT IN ('Junior', 'Mid-Level', 'Senior', 'Executive')")

    # Work location and job arrangement updates
    op.execute("UPDATE jobs SET work_location = 'Office' WHERE work_location NOT IN ('Remote', 'Hybrid', 'Office')")
    op.execute("UPDATE jobs SET job_arrangement = 'Permanent' WHERE job_arrangement NOT IN ('Permanent', 'Contract/Temp', 'Internship', 'Part-Time')")

    # Alter column types to use the newly created ENUMs
    with op.batch_alter_table('jobs', schema=None) as batch_op:
        batch_op.alter_column('specialization',
                              existing_type=sa.VARCHAR(length=255),
                              type_=specialization_enum,
                              postgresql_using="specialization::specialization_enum",
                              existing_nullable=True)
        batch_op.alter_column('work_location',
                              existing_type=sa.VARCHAR(length=20),
                              type_=work_location_enum,
                              postgresql_using="work_location::work_location_enum",
                              existing_nullable=True)
        batch_op.alter_column('experience_level',
                              existing_type=sa.VARCHAR(length=50),
                              type_=experience_level_enum,
                              postgresql_using="experience_level::experience_level_enum",
                              existing_nullable=True)
        batch_op.alter_column('job_arrangement',
                              existing_type=sa.VARCHAR(length=255),
                              type_=job_arrangement_enum,
                              postgresql_using="job_arrangement::job_arrangement_enum",
                              existing_nullable=True)

def downgrade():
    # Logic to downgrade ENUM changes if necessary
    pass
