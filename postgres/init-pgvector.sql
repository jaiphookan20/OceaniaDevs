-- Connect to the job_board database
\c job_board;

-- Create the vector extension
CREATE EXTENSION IF NOT EXISTS vector;

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

    -- salary_range_enum
    IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'salary_range_type') THEN
        CREATE TYPE salary_range_type AS ENUM (
            '20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000',
            '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000',
            '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+'
        );
    END IF;
END$$;