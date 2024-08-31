"""Update existing specialization data

Revision ID: 60b5058d0026
Revises: 1c7d58b5de1d
Create Date: 2024-08-27 11:37:38.454104

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = '60b5058d0026'
down_revision = '1c7d58b5de1d'
branch_labels = None
depends_on = None

def upgrade():
    # Step 1: Convert specialization to text
    op.execute("ALTER TABLE jobs ALTER COLUMN specialization TYPE text USING specialization::text")

    # Step 2: Update the data
    op.execute("UPDATE jobs SET specialization = 'DevOps' WHERE specialization = 'DevOps & IT'")
    op.execute("UPDATE jobs SET specialization = 'Cloud & Infra' WHERE specialization = 'Cloud & Infrastructure'")
    op.execute("UPDATE jobs SET specialization = 'Data & ML' WHERE specialization IN ('Business Intelligence & Data', 'Machine Learning & AI')")
    op.execute("UPDATE jobs SET specialization = 'Full-Stack' WHERE specialization = 'Business Application Development'")
    
    # Handle any remaining non-conforming values
    op.execute("UPDATE jobs SET specialization = 'Full-Stack' WHERE specialization NOT IN ('Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity')")

    # Step 3: Create new enum type
    op.execute("DROP TYPE IF EXISTS specialization_enum")
    op.execute("CREATE TYPE specialization_enum AS ENUM ('Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity')")

    # Step 4: Convert column back to enum
    op.execute("ALTER TABLE jobs ALTER COLUMN specialization TYPE specialization_enum USING specialization::specialization_enum")

    # Drop the 'city' column from the 'candidates' table
    op.execute("ALTER TABLE candidates DROP COLUMN IF EXISTS city")

def downgrade():
    # Convert back to text if needed
    op.execute("ALTER TABLE jobs ALTER COLUMN specialization TYPE text USING specialization::text")
    
    # Recreate the original enum if needed
    op.execute("DROP TYPE IF EXISTS specialization_enum")
    op.execute("CREATE TYPE specialization_enum AS ENUM ('Frontend', 'Backend', 'Full-Stack', 'DevOps & IT', 'Cloud & Infrastructure', 'Business Intelligence & Data', 'Machine Learning & AI', 'Mobile', 'Cybersecurity', 'Business Application Development', 'Project Management', 'QA & Testing')")

    # Convert back to the original enum
    op.execute("ALTER TABLE jobs ALTER COLUMN specialization TYPE specialization_enum USING specialization::specialization_enum")

    # Add back the 'city' column to the 'candidates' table if needed
    op.execute("ALTER TABLE candidates ADD COLUMN IF NOT EXISTS city VARCHAR(255)")