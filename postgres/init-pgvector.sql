-- Connect to the job_board database
\c job_board;



-- Create extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

\echo 'Starting init-pgvector.sql execution'

-- Create enum types
DO $$
BEGIN
    -- state_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state_enum') THEN
        CREATE TYPE state_enum AS ENUM ('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA');
    END IF;

    -- country_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'country_enum') THEN
        CREATE TYPE country_enum AS ENUM ('Australia', 'New Zealand');
    END IF;

    -- Change: job_type to job_type_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_type_enum') THEN
        CREATE TYPE job_type_enum AS ENUM ('premium', 'normal');
    END IF;

    -- Change: industry_type to industry_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'industry_enum') THEN
        CREATE TYPE industry_enum AS ENUM (
            'Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare',
            'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity',
            'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive',
            'Construction', 'Education', 'Energy & Utilities', 'Entertainment',
            'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising',
            'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate',
            'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics'
        );
    END IF;

    -- Change: salary_range_type to salary_range_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'salary_range_enum') THEN
        CREATE TYPE salary_range_enum AS ENUM (
            'Not Listed', '20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000',
            '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000',
            '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+'
        );
    END IF;

    -- specialization_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'specialization_enum') THEN
        CREATE TYPE specialization_enum AS ENUM (
            'Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing',
            'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity'
        );
    END IF;

    -- experience_level_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'experience_level_enum') THEN
        CREATE TYPE experience_level_enum AS ENUM (
            'Junior', 'Mid-Level', 'Senior', 'Executive'
        );
    END IF;

    -- work_location_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'work_location_enum') THEN
        CREATE TYPE work_location_enum AS ENUM (
            'Remote', 'Hybrid', 'Office'
        );
    END IF;

    -- job_arrangement_enum (no change needed)
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_arrangement_enum') THEN
        CREATE TYPE job_arrangement_enum AS ENUM (
            'Permanent', 'Contract/Temp', 'Internship', 'Part-Time'
        );
    END IF;

    -- salary_type_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'salary_type_enum') THEN
        CREATE TYPE salary_type_enum AS ENUM ('annual', 'hourly', 'daily');
    END IF;

    -- contract_duration_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'contract_duration_enum') THEN
        CREATE TYPE contract_duration_enum AS ENUM ('Not Listed', '0-3 months', '4-6 months', '7-9 months', '10-12 months', '12+ months');
    END IF;

    -- daily_range_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'daily_range_enum') THEN
        CREATE TYPE daily_range_enum AS ENUM ('Not Listed', '0-200', '200-400', '400-600', '600-800', '800-1000', '1000-1200', '1200-1400', '1400-1600', '1600+');
    END IF;

    -- hourly_range_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'hourly_range_enum') THEN
        CREATE TYPE hourly_range_enum AS ENUM ('Not Listed', '0-20', '20-40', '40-60', '60-80', '80-100', '100-120', '120-140', '140-160', '160+');
    END IF;
END$$;

-- Create tables if they don't exist
CREATE TABLE IF NOT EXISTS seekers (
    uid SERIAL PRIMARY KEY,
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(128),
    city VARCHAR(255),
    state state_enum,
    country country_enum,
    datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE IF NOT EXISTS companies (
    company_id SERIAL PRIMARY KEY,
    name VARCHAR(255) NOT NULL,
    website_url VARCHAR(255),
    country country_enum,
    size VARCHAR(100),
    address VARCHAR(255),
    description TEXT,
    logo_url VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    industry industry_enum,
    state state_enum,
    city VARCHAR(255),
    type VARCHAR(255),
    name_vector TSVECTOR
);

CREATE TABLE IF NOT EXISTS recruiters (
    recruiter_id SERIAL PRIMARY KEY,
    company_id INTEGER REFERENCES companies(company_id),
    first_name VARCHAR(255),
    last_name VARCHAR(255),
    position VARCHAR(255),
    email VARCHAR(255) NOT NULL,
    password VARCHAR(255),
    city VARCHAR(255),
    state state_enum,
    country country_enum,
    is_direct_recruiter BOOLEAN,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    email_verified BOOLEAN DEFAULT FALSE,
    verification_code VARCHAR(6),
    verification_code_expiry TIMESTAMP
);

CREATE TABLE IF NOT EXISTS jobs (
    job_id SERIAL PRIMARY KEY,
    recruiter_id INTEGER REFERENCES recruiters(recruiter_id),
    company_id INTEGER REFERENCES companies(company_id),
    title VARCHAR(255) NOT NULL,
    city VARCHAR(255),
    state VARCHAR(255),
    country VARCHAR(255),
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    expiry_date DATE DEFAULT (CURRENT_DATE + INTERVAL '30 days'),
    jobpost_url VARCHAR(255),
    description TEXT,
    overview TEXT,
    responsibilities TEXT,
    requirements TEXT,
    work_location work_location_enum,
    work_rights VARCHAR[],
    job_arrangement job_arrangement_enum,
    specialization specialization_enum,
    job_type job_type_enum DEFAULT 'normal',
    industry industry_enum NOT NULL,
    min_experience_years INTEGER,
    experience_level experience_level_enum,
    tech_stack VARCHAR[],
    salary_range salary_range_enum,
    salary_type salary_type_enum DEFAULT 'annual',
    contract_duration contract_duration_enum DEFAULT 'Not Listed',
    daily_range daily_range_enum DEFAULT 'Not Listed',
    hourly_range hourly_range_enum DEFAULT 'Not Listed',
    citizens_or_pr_only BOOLEAN DEFAULT FALSE,
    security_clearance_required BOOLEAN DEFAULT FALSE,
    search_vector TSVECTOR,
    embedding vector(1536)
);

CREATE TABLE IF NOT EXISTS technologies (
    id SERIAL PRIMARY KEY,
    name VARCHAR UNIQUE NOT NULL,
    name_vector TSVECTOR
);

CREATE TABLE IF NOT EXISTS technology_aliases (
    alias VARCHAR PRIMARY KEY,
    technology_id INTEGER REFERENCES technologies(id) NOT NULL
);

CREATE TABLE IF NOT EXISTS job_technologies (
    job_id INTEGER REFERENCES jobs(job_id),
    technology_id INTEGER REFERENCES technologies(id),
    PRIMARY KEY (job_id, technology_id)
);

CREATE TABLE IF NOT EXISTS candidates (
    candidate_id SERIAL PRIMARY KEY,
    name VARCHAR(255),
    years_experience INTEGER,
    position VARCHAR(255),
    work_experience VARCHAR(800),
    favorite_languages VARCHAR[],
    technologies VARCHAR[],
    embedding vector(1536)
);

CREATE TABLE IF NOT EXISTS applications (
    applicationid SERIAL PRIMARY KEY,
    userid INTEGER REFERENCES seekers(uid),
    jobid INTEGER REFERENCES jobs(job_id),
    datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    status VARCHAR(50) DEFAULT 'Applied'
);

CREATE TABLE IF NOT EXISTS bookmarks (
    bookmarksid SERIAL PRIMARY KEY,
    userid INTEGER REFERENCES seekers(uid),
    jobid INTEGER REFERENCES jobs(job_id),
    datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Create or replace functions for search vector updates
CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
DECLARE
    company_name TEXT;
    company_description TEXT;
BEGIN
    -- Get the company name and description
    SELECT name, description INTO company_name, company_description 
    FROM companies 
    WHERE company_id = NEW.company_id;
    
    NEW.search_vector :=
        setweight(to_tsvector('english', coalesce(NEW.title,'')), 'A') ||
        setweight(to_tsvector('english', coalesce(NEW.description,'')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.overview,'')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.responsibilities,'')), 'B') ||
        setweight(to_tsvector('english', coalesce(NEW.requirements,'')), 'B') ||
        setweight(to_tsvector('english', coalesce(company_name,'')), 'C') ||
        setweight(to_tsvector('english', coalesce(company_description,'')), 'D');
    RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION company_name_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.name_vector := to_tsvector('english', coalesce(NEW.name,''));
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

CREATE OR REPLACE FUNCTION technology_name_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.name_vector := to_tsvector('english', coalesce(NEW.name,''));
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

-- Create triggers
DROP TRIGGER IF EXISTS jobs_search_vector_update ON jobs;
CREATE TRIGGER jobs_search_vector_update
BEFORE INSERT OR UPDATE ON jobs
FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();

DROP TRIGGER IF EXISTS company_name_vector_update ON companies;
CREATE TRIGGER company_name_vector_update
BEFORE INSERT OR UPDATE ON companies
FOR EACH ROW EXECUTE FUNCTION company_name_vector_update();

DROP TRIGGER IF EXISTS technology_name_vector_update ON technologies;
CREATE TRIGGER technology_name_vector_update
BEFORE INSERT OR UPDATE ON technologies
FOR EACH ROW EXECUTE FUNCTION technology_name_vector_update();

-- -- Add vector columns if they don't exist
-- DO $$
-- BEGIN
--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'search_vector') THEN
--     ALTER TABLE jobs ADD COLUMN search_vector tsvector;
--   END IF;
  
--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'companies' AND column_name = 'name_vector') THEN
--     ALTER TABLE companies ADD COLUMN name_vector tsvector;
--   END IF;
  
--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'technologies' AND column_name = 'name_vector') THEN
--     ALTER TABLE technologies ADD COLUMN name_vector tsvector;
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'embedding') THEN
--     ALTER TABLE jobs ADD COLUMN embedding vector(1536);
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'candidates' AND column_name = 'embedding') THEN
--     ALTER TABLE candidates ADD COLUMN embedding vector(1536);
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'citizens_or_pr_only') THEN
--     ALTER TABLE jobs ADD COLUMN citizens_or_pr_only BOOLEAN DEFAULT FALSE;
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'security_clearance_required') THEN
--     ALTER TABLE jobs ADD COLUMN security_clearance_required BOOLEAN DEFAULT FALSE;
--   END IF;

--     IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'salary_type') THEN
--     ALTER TABLE jobs ADD COLUMN salary_type salary_type_enum DEFAULT 'annual';
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'contract_duration') THEN
--     ALTER TABLE jobs ADD COLUMN contract_duration contract_duration_enum DEFAULT 'Not Listed';
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'daily_range') THEN
--     ALTER TABLE jobs ADD COLUMN daily_range daily_range_enum DEFAULT 'Not Listed';
--   END IF;

--   IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'hourly_range') THEN
--     ALTER TABLE jobs ADD COLUMN hourly_range hourly_range_enum DEFAULT 'Not Listed';
--   END IF;
-- END$$;

-- Create GIN indexes
\echo 'Creating or verifying GIN indexes...'

DO $$
DECLARE
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_search_vector_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_search_vector_idx ON jobs USING GIN (search_vector);
        RAISE NOTICE 'Created index: jobs_search_vector_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_search_vector_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'companies_name_vector_idx';
    IF index_count = 0 THEN
        CREATE INDEX companies_name_vector_idx ON companies USING GIN (name_vector);
        RAISE NOTICE 'Created index: companies_name_vector_idx';
    ELSE
        RAISE NOTICE 'Index already exists: companies_name_vector_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'technologies_name_vector_idx';
    IF index_count = 0 THEN
        CREATE INDEX technologies_name_vector_idx ON technologies USING GIN (name_vector);
        RAISE NOTICE 'Created index: technologies_name_vector_idx';
    ELSE
        RAISE NOTICE 'Index already exists: technologies_name_vector_idx';
    END IF;
END $$;

\echo 'Creating or verifying B-tree indexes...'

DO $$
DECLARE
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_specialization_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_specialization_idx ON jobs (specialization);
        RAISE NOTICE 'Created index: jobs_specialization_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_specialization_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_experience_level_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_experience_level_idx ON jobs (experience_level);
        RAISE NOTICE 'Created index: jobs_experience_level_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_experience_level_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_work_location_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_work_location_idx ON jobs (work_location);
        RAISE NOTICE 'Created index: jobs_work_location_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_work_location_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_city_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_city_idx ON jobs (city);
        RAISE NOTICE 'Created index: jobs_city_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_city_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'job_technologies_job_id_idx';
    IF index_count = 0 THEN
        CREATE INDEX job_technologies_job_id_idx ON job_technologies (job_id);
        RAISE NOTICE 'Created index: job_technologies_job_id_idx';
    ELSE
        RAISE NOTICE 'Index already exists: job_technologies_job_id_idx';
    END IF;

    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'job_technologies_technology_id_idx';
    IF index_count = 0 THEN
        CREATE INDEX job_technologies_technology_id_idx ON job_technologies (technology_id);
        RAISE NOTICE 'Created index: job_technologies_technology_id_idx';
    ELSE
        RAISE NOTICE 'Index already exists: job_technologies_technology_id_idx';
    END IF;
END $$;

-- Update existing rows
\echo 'Updating existing rows...'
UPDATE companies SET name_vector = to_tsvector('english', coalesce(name,''));
UPDATE technologies SET name_vector = to_tsvector('english', coalesce(name,''));

-- This is the correct, comprehensive update for jobs:
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

\echo 'Finished init-pgvector.sql execution'

/*
@init-pgvector.sql Explain to me in detail everything that is happening here in this file, because I don't understand at all.

Certainly! I'll break down the init-pgvector.sql file section by section:
Database Connection and Extensions:
\c job_board;
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

This connects to the 'job_board' database and ensures the 'vector' and 'pg_trgm' extensions are installed. These extensions are needed for vector operations and text similarity searches.
Enum Types Creation:
DO $$
BEGIN
    -- state_enum, country_enum, job_type_enum, etc.
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state_enum') THEN
        CREATE TYPE state_enum AS ENUM ('VIC', 'NSW', ...);
    END IF;
    -- ... (other enum types)
END$$;

This block creates various ENUM types if they don't already exist. ENUMs are custom data types that allow a column to have a predefined set of values.

Function Definitions:
CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
-- ... function body ...
$$ LANGUAGE plpgsql;

These functions are used to update search vectors. They're called by triggers when data is inserted or updated in certain tables.

Trigger Creation:
DROP TRIGGER IF EXISTS jobs_search_vector_update ON jobs;
CREATE TRIGGER jobs_search_vector_update
BEFORE INSERT OR UPDATE ON jobs
FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();

These create triggers that automatically call the functions defined earlier when data is inserted or updated in the respective tables.
Adding Vector Columns:
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'search_vector') THEN
    ALTER TABLE jobs ADD COLUMN search_vector tsvector;
  END IF;
  -- ... (similar for other tables)
END$$;

This block adds vector columns to tables if they don't already exist. These columns are used for full-text search and vector operations.

Creating Indexes:
DO $$
DECLARE
    index_count INT;
BEGIN
    SELECT COUNT(*) INTO index_count FROM pg_indexes WHERE indexname = 'jobs_search_vector_idx';
    IF index_count = 0 THEN
        CREATE INDEX jobs_search_vector_idx ON jobs USING GIN (search_vector);
        RAISE NOTICE 'Created index: jobs_search_vector_idx';
    ELSE
        RAISE NOTICE 'Index already exists: jobs_search_vector_idx';
    END IF;
    -- ... (similar for other indexes)
END $$;
This creates various indexes if they don't already exist. Indexes improve query performance for searching and filtering.

Updating Existing Rows:
UPDATE companies SET name_vector = to_tsvector('english', coalesce(name,''));
UPDATE technologies SET name_vector = to_tsvector('english', coalesce(name,''));

UPDATE jobs j
SET search_vector = subquery.new_search_vector
FROM (
    -- ... complex query ...
) AS subquery
WHERE j.job_id = subquery.job_id;
;
These statements update the vector columns for existing rows in the database, ensuring all current data has the appropriate search vectors.
In summary, this script sets up the database structure for efficient text search and vector operations. It creates custom data types, sets up automatic updating of search vectors, adds necessary columns, creates performance-enhancing indexes, and ensures all existing data is properly formatted for these new features. This script is designed to be run multiple times safely, only making changes when necessary.

*/