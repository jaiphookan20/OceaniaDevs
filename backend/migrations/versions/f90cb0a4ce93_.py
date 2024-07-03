"""empty message

Revision ID: f90cb0a4ce93
Revises: 
Create Date: 2024-04-28 19:04:51.824648

"""
from alembic import op
import sqlalchemy as sa
from sqlalchemy.sql import text
from pgvector.sqlalchemy import Vector  # Ensure pgvector is imported

# revision identifiers, used by Alembic.
revision = 'f90cb0a4ce93'
down_revision = None
branch_labels = None
depends_on = None

def column_exists(conn, table_name, column_name):
    query = text("""
        SELECT EXISTS (
            SELECT 1
            FROM information_schema.columns 
            WHERE table_name=:table_name AND column_name=:column_name
        )
    """)
    res = conn.execute(query, {'table_name': table_name, 'column_name': column_name})
    return res.scalar()

def upgrade():
    conn = op.get_bind()

    # Ensure the pgvector extension is created
    op.execute('CREATE EXTENSION IF NOT EXISTS vector')

    # Check if the enum 'state_enum' exists before attempting to create it
    res = conn.execute(text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state_enum')"))
    if not res.scalar():
        op.execute("CREATE TYPE state_enum AS ENUM('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA')")

    # Check if the enum 'country_enum' exists before attempting to create it
    res = conn.execute(text("SELECT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'country_enum')"))
    if not res.scalar():
        op.execute("CREATE TYPE country_enum AS ENUM('Australia', 'New Zealand')")

    # Seeker Table Changes
    if not column_exists(conn, 'seekers', 'city'):
        op.add_column('seekers', sa.Column('city', sa.String(length=255), nullable=True))
    if not column_exists(conn, 'seekers', 'state'):
        op.add_column('seekers', sa.Column('state', sa.Enum('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'), nullable=True))
    if not column_exists(conn, 'seekers', 'country'):
        op.add_column('seekers', sa.Column('country', sa.Enum('Australia', 'New Zealand', name='country_enum'), nullable=True))
    if not column_exists(conn, 'seekers', 'first_name'):
        op.add_column('seekers', sa.Column('first_name', sa.String, nullable=True))
    if not column_exists(conn, 'seekers', 'last_name'):
        op.add_column('seekers', sa.Column('last_name', sa.String, nullable=True))

    # Recruiter Table Changes
    if not column_exists(conn, 'recruiters', 'first_name'):
        op.add_column('recruiters', sa.Column('first_name', sa.String, nullable=True))
    if not column_exists(conn, 'recruiters', 'last_name'):
        op.add_column('recruiters', sa.Column('last_name', sa.String, nullable=True))
    if not column_exists(conn, 'recruiters', 'password'):
        op.add_column('recruiters', sa.Column('password', sa.String, nullable=True))

    # Check if the embedding column exists in the candidates table, and if not, add it
    if not column_exists(conn, 'candidates', 'embedding'):
        op.add_column('candidates', sa.Column('embedding', Vector(1536)))
    else:
        op.execute('ALTER TABLE candidates ALTER COLUMN embedding TYPE vector USING embedding::vector')

    # Check if the embedding column exists in the jobs table, and if not, add it
    if not column_exists(conn, 'jobs', 'embedding'):
        op.add_column('jobs', sa.Column('embedding', Vector(1536)))
    else:
        op.execute('ALTER TABLE jobs ALTER COLUMN embedding TYPE vector USING embedding::vector')

def downgrade():
    conn = op.get_bind()

    # Seeker Table Changes
    if column_exists(conn, 'seekers', 'city'):
        op.drop_column('seekers', 'city')
    if column_exists(conn, 'seekers', 'state'):
        op.drop_column('seekers', 'state')
    if column_exists(conn, 'seekers', 'country'):
        op.drop_column('seekers', 'country')
    if column_exists(conn, 'seekers', 'first_name'):
        op.drop_column('seekers', 'first_name')
    if column_exists(conn, 'seekers', 'last_name'):
        op.drop_column('seekers', 'last_name')

    # Recruiter Table Changes
    if column_exists(conn, 'recruiters', 'first_name'):
        op.drop_column('recruiters', 'first_name')
    if column_exists(conn, 'recruiters', 'last_name'):
        op.drop_column('recruiters', 'last_name')
    if column_exists(conn, 'recruiters', 'password'):
        op.drop_column('recruiters', 'password')

    # Alter the embedding column type back to the previous type in candidates and jobs tables
    if column_exists(conn, 'candidates', 'embedding'):
        op.execute('ALTER TABLE candidates ALTER COLUMN embedding TYPE varchar(255) USING embedding::varchar')
    if column_exists(conn, 'jobs', 'embedding'):
        op.execute('ALTER TABLE jobs ALTER COLUMN embedding TYPE varchar(255) USING embedding::varchar')

    op.execute('DROP EXTENSION IF EXISTS vector')
    op.execute('DROP TYPE IF EXISTS country_enum CASCADE')
    op.execute('DROP TYPE IF EXISTS state_enum CASCADE')
    # ### end Alembic commands ###
