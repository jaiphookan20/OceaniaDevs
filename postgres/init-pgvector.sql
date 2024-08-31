-- Connect to the job_board database
\c job_board;

-- Create the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

-- Create the text search configuration
CREATE EXTENSION IF NOT EXISTS pg_trgm;

-- Log the start of the script execution
\echo 'Starting init-pgvector.sql execution'

-- Create enum types
DO $$
BEGIN
    -- state_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'state_enum') THEN
        CREATE TYPE state_enum AS ENUM ('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA');
    END IF;

    -- country_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'country_enum') THEN
        CREATE TYPE country_enum AS ENUM ('Australia', 'New Zealand');
    END IF;

    -- job_type_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_type') THEN
        CREATE TYPE job_type AS ENUM ('premium', 'normal');
    END IF;

    -- industry_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'industry_type') THEN
        CREATE TYPE industry_type AS ENUM (
            'Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare',
            'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity',
            'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive',
            'Construction', 'Education', 'Energy & Utilities', 'Entertainment',
            'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising',
            'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate',
            'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics'
        );
    END IF;

    -- Updated salary_range_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'salary_range_type') THEN
        CREATE TYPE salary_range_type AS ENUM (
            'Not Listed', '20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000',
            '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000',
            '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+'
        );
    END IF;

    -- New specialization_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'specialization_enum') THEN
        CREATE TYPE specialization_enum AS ENUM (
            'Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing',
            'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity'
        );
    END IF;

    -- New experience_level_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'experience_level_enum') THEN
        CREATE TYPE experience_level_enum AS ENUM (
            'Junior', 'Mid-Level', 'Senior', 'Executive'
        );
    END IF;

    -- New work_location_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'work_location_enum') THEN
        CREATE TYPE work_location_enum AS ENUM (
            'Remote', 'Hybrid', 'Office'
        );
    END IF;

    -- New job_arrangement_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_arrangement_enum') THEN
        CREATE TYPE job_arrangement_enum AS ENUM (
            'Permanent', 'Contract/Temp', 'Internship', 'Part-Time'
        );
    END IF;
END$$;

-- Create or replace the function to update the search_vector
CREATE OR REPLACE FUNCTION jobs_search_vector_update() RETURNS trigger AS $$
BEGIN
  NEW.search_vector :=
    setweight(to_tsvector('english', coalesce(NEW.title,'')), 'A') ||
    setweight(to_tsvector('english', coalesce(NEW.description,'')), 'C') ||
    -- setweight(to_tsvector('english', coalesce(NEW.specialization,'')), 'C') ||
    -- setweight(to_tsvector('english', coalesce(NEW.city,'')), 'D') ||
    -- setweight(to_tsvector('english', coalesce(NEW.state::text,'')), 'D') ||
    -- setweight(to_tsvector('english', coalesce(NEW.country::text,'')), 'D') ||
    setweight(to_tsvector('english', coalesce(array_to_string(NEW.tech_stack, ' '),'')), 'C');
  RETURN NEW;
END
$$ LANGUAGE plpgsql;

-- Log function creation
\echo 'Function jobs_search_vector_update created'

-- Drop the trigger if it exists and recreate it
DROP TRIGGER IF EXISTS jobs_search_vector_update ON jobs;
CREATE TRIGGER jobs_search_vector_update
BEFORE INSERT OR UPDATE ON jobs
FOR EACH ROW EXECUTE FUNCTION jobs_search_vector_update();

-- Log trigger creation
\echo 'Trigger jobs_search_vector_update created'

-- Add search_vector column if it doesn't exist
DO $$
BEGIN
  IF NOT EXISTS (
    SELECT 1
    FROM information_schema.columns
    WHERE table_name = 'jobs' AND column_name = 'search_vector'
  ) THEN
    ALTER TABLE jobs ADD COLUMN search_vector tsvector;
    RAISE NOTICE 'search_vector column added to jobs table';
  ELSE
    RAISE NOTICE 'search_vector column already exists in jobs table';
  END IF;
END$$;

-- Create a GIN index on the search_vector for faster searching
CREATE INDEX IF NOT EXISTS jobs_search_vector_idx ON jobs USING GIN (search_vector);

-- Log index creation
\echo 'GIN index jobs_search_vector_idx created or already exists'

-- Update existing rows
UPDATE jobs SET search_vector = NULL;
UPDATE jobs SET
  search_vector = 
    setweight(to_tsvector('english', coalesce(title,'')), 'A') ||
    setweight(to_tsvector('english', coalesce(description,'')), 'C') ||
    -- setweight(to_tsvector('english', coalesce(specialization,'')), 'C') ||
    -- setweight(to_tsvector('english', coalesce(city,'')), 'D') ||
    -- setweight(to_tsvector('english', coalesce(state::text,'')), 'D') ||
    -- setweight(to_tsvector('english', coalesce(country::text,'')), 'D') ||
    setweight(to_tsvector('english', coalesce(array_to_string(tech_stack, ' '),'')), 'B');

-- Log completion of updates
\echo 'Existing rows updated with search_vector'

-- Log the end of the script execution
\echo 'Finished init-pgvector.sql execution'