"""Create ENUM types and initial tables

Revision ID: e82c1afce43c
Revises: 
Create Date: 2024-07-01 20:46:56.018371

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql

# revision identifiers, used by Alembic.
revision = 'e82c1afce43c'
down_revision = None
branch_labels = None
depends_on = None

def create_enum_if_not_exists(enum_name, enum_values):
    op.execute(f"""
    DO $$
    BEGIN
        IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = '{enum_name}') THEN
            CREATE TYPE {enum_name} AS ENUM {enum_values};
        END IF;
    END$$;
    """)

def upgrade():
   def upgrade():
    # Create ENUM types
    create_enum_if_not_exists('state_enum', "('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA')")
    create_enum_if_not_exists('country_enum', "('Australia', 'New Zealand')")
    create_enum_if_not_exists('job_type', "('premium', 'normal')")
    create_enum_if_not_exists('industry_type', "('Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics')")
    create_enum_if_not_exists('salary_range_type', "('20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+')")

    # Create tables
    op.create_table('companies',
    sa.Column('company_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=False),
    sa.Column('website_url', sa.String(length=255), nullable=True),
    sa.Column('country', sa.Enum('Australia', 'New Zealand', name='country_enum'), nullable=True),
    sa.Column('size', sa.String(length=100), nullable=True),
    sa.Column('address', sa.String(length=255), nullable=True),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('logo_url', sa.String(length=255), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.PrimaryKeyConstraint('company_id')
    )
    op.create_table('recruiters',
    sa.Column('recruiter_id', sa.Integer(), nullable=False),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('position', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password', sa.String(length=255), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.Enum('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'), nullable=True),
    sa.Column('country', sa.Enum('Australia', 'New Zealand', name='country_enum'), nullable=True),
    sa.Column('is_direct_recruiter', sa.Boolean(), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.PrimaryKeyConstraint('recruiter_id')
    )

    op.create_table('seekers',
    sa.Column('uid', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=255), nullable=True),
    sa.Column('last_name', sa.String(length=255), nullable=True),
    sa.Column('email', sa.String(length=255), nullable=False),
    sa.Column('password_hash', sa.String(length=128), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.Enum('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'), nullable=True),
    sa.Column('country', sa.Enum('Australia', 'New Zealand', name='country_enum'), nullable=True),
    sa.Column('datetimestamp', sa.DateTime(), nullable=True),
    sa.PrimaryKeyConstraint('uid'),
    sa.UniqueConstraint('email')
    )

    op.create_table('jobs',
    sa.Column('job_id', sa.Integer(), nullable=False),
    sa.Column('recruiter_id', sa.Integer(), nullable=True),
    sa.Column('company_id', sa.Integer(), nullable=True),
    sa.Column('title', sa.String(length=255), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('specialization', sa.String(length=255), nullable=True),
    sa.Column('job_type', sa.Enum('premium', 'normal', name='job_type'), nullable=True),
    sa.Column('industry', sa.Enum('Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics', name='industry_type'), nullable=False),
    sa.Column('salary_range', sa.Enum('20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+', name='salary_range_type'), nullable=True),
    sa.Column('salary_type', sa.String(length=10), nullable=True),
    sa.Column('work_location', sa.String(length=20), nullable=True),
    sa.Column('min_experience_years', sa.Integer(), nullable=True),
    sa.Column('experience_level', sa.String(length=50), nullable=True),
    sa.Column('tech_stack', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('city', sa.String(length=255), nullable=True),
    sa.Column('state', sa.String(length=255), nullable=True),
    sa.Column('country', sa.String(length=255), nullable=True),
    sa.Column('expiry_date', sa.Date(), server_default=sa.text("CURRENT_DATE + INTERVAL '30 days'"), nullable=True),
    sa.Column('jobpost_url', sa.String(length=255), nullable=True),
    sa.Column('work_rights', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('created_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('updated_at', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.Column('search_vector', postgresql.TSVECTOR(), nullable=True),
    sa.Column('embedding', postgresql.VECTOR(dimensions=1536), nullable=True),
    sa.ForeignKeyConstraint(['company_id'], ['companies.company_id'], ),
    sa.ForeignKeyConstraint(['recruiter_id'], ['recruiters.recruiter_id'], ),
    sa.PrimaryKeyConstraint('job_id')
    )

    op.create_table('candidates',
    sa.Column('candidate_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=255), nullable=True),
    sa.Column('years_experience', sa.Integer(), nullable=True),
    sa.Column('position', sa.String(length=255), nullable=True),
    sa.Column('work_experience', sa.String(length=800), nullable=True),
    sa.Column('favorite_languages', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('technologies', sa.ARRAY(sa.String()), nullable=True),
    sa.Column('embedding', postgresql.VECTOR(dimensions=1536), nullable=True),
    sa.PrimaryKeyConstraint('candidate_id')
    )

    op.create_table('applications',
    sa.Column('applicationid', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('jobid', sa.Integer(), nullable=True),
    sa.Column('datetimestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['jobid'], ['jobs.job_id'], ),
    sa.ForeignKeyConstraint(['userid'], ['seekers.uid'], ),
    sa.PrimaryKeyConstraint('applicationid')
    )

    op.create_table('bookmarks',
    sa.Column('bookmarksid', sa.Integer(), nullable=False),
    sa.Column('userid', sa.Integer(), nullable=True),
    sa.Column('jobid', sa.Integer(), nullable=True),
    sa.Column('datetimestamp', sa.DateTime(), server_default=sa.text('now()'), nullable=True),
    sa.ForeignKeyConstraint(['jobid'], ['jobs.job_id'], ),
    sa.ForeignKeyConstraint(['userid'], ['seekers.uid'], ),
    sa.PrimaryKeyConstraint('bookmarksid')
    )


def downgrade():
    # Drop tables
    op.drop_table('bookmarks')
    op.drop_table('applications')
    op.drop_table('candidates')
    op.drop_table('jobs')
    op.drop_table('seekers')
    op.drop_table('recruiters')
    op.drop_table('companies')

    # Drop ENUM types
    op.execute("DROP TYPE IF EXISTS state_enum")
    op.execute("DROP TYPE IF EXISTS country_enum")
    op.execute("DROP TYPE IF EXISTS job_type")
    op.execute("DROP TYPE IF EXISTS industry_type")
    op.execute("DROP TYPE IF EXISTS salary_range_type")