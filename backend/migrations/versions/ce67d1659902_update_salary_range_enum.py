"""Update salary_range_enum

Revision ID: ce67d1659902
Revises: 60b5058d0026
Create Date: 2024-08-27 12:15:11.094851

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'ce67d1659902'
down_revision = '60b5058d0026'
branch_labels = None
depends_on = None


def upgrade():
    # Convert salary_range to text
    op.execute("ALTER TABLE jobs ALTER COLUMN salary_range TYPE text USING salary_range::text")

    # Update NULL values to 'Not Listed'
    op.execute("UPDATE jobs SET salary_range = 'Not Listed' WHERE salary_range IS NULL")

    # Create new enum type
    op.execute("DROP TYPE IF EXISTS salary_range_type")
    op.execute("CREATE TYPE salary_range_type AS ENUM ('Not Listed', '20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+')")

    # Convert column back to enum
    op.execute("ALTER TABLE jobs ALTER COLUMN salary_range TYPE salary_range_type USING salary_range::salary_range_type")

def downgrade():
    # Convert salary_range to text
    op.execute("ALTER TABLE jobs ALTER COLUMN salary_range TYPE text USING salary_range::text")

    # Remove 'Not Listed' values
    op.execute("UPDATE jobs SET salary_range = NULL WHERE salary_range = 'Not Listed'")

    # Recreate original enum
    op.execute("DROP TYPE IF EXISTS salary_range_type")
    op.execute("CREATE TYPE salary_range_type AS ENUM ('20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+')")

    # Convert column back to enum
    op.execute("ALTER TABLE jobs ALTER COLUMN salary_range TYPE salary_range_type USING salary_range::salary_range_type")