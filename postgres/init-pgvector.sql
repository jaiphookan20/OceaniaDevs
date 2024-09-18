-- Connect to the job_board database
\c job_board;

-- Create extensions
CREATE EXTENSION IF NOT EXISTS vector;
CREATE EXTENSION IF NOT EXISTS pg_trgm;

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

-- Add vector columns if they don't exist
DO $$
BEGIN
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'search_vector') THEN
    ALTER TABLE jobs ADD COLUMN search_vector tsvector;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'companies' AND column_name = 'name_vector') THEN
    ALTER TABLE companies ADD COLUMN name_vector tsvector;
  END IF;
  
  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'technologies' AND column_name = 'name_vector') THEN
    ALTER TABLE technologies ADD COLUMN name_vector tsvector;
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'embedding') THEN
    ALTER TABLE jobs ADD COLUMN embedding vector(1536);
  END IF;

  IF NOT EXISTS (SELECT 1 FROM information_schema.columns WHERE table_name = 'candidates' AND column_name = 'embedding') THEN
    ALTER TABLE candidates ADD COLUMN embedding vector(1536);
  END IF;
END$$;

-- Create GIN indexes
CREATE INDEX IF NOT EXISTS jobs_search_vector_idx ON jobs USING GIN (search_vector);
CREATE INDEX IF NOT EXISTS companies_name_vector_idx ON companies USING GIN (name_vector);
CREATE INDEX IF NOT EXISTS technologies_name_vector_idx ON technologies USING GIN (name_vector);

-- Add after the existing CREATE INDEX statements

-- For frequently used filters in filtered_search_jobs
CREATE INDEX IF NOT EXISTS jobs_specialization_idx ON jobs (specialization);
CREATE INDEX IF NOT EXISTS jobs_experience_level_idx ON jobs (experience_level);
CREATE INDEX IF NOT EXISTS jobs_work_location_idx ON jobs (work_location);
CREATE INDEX IF NOT EXISTS jobs_city_idx ON jobs (city);

-- For tech stack filtering
CREATE INDEX IF NOT EXISTS job_technologies_job_id_idx ON job_technologies (job_id);
CREATE INDEX IF NOT EXISTS job_technologies_technology_id_idx ON job_technologies (technology_id);

-- Update existing rows
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