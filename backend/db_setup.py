import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

def setup_tables():
    conn = psycopg2.connect(
        host=DB_HOST,
        port="5432",
        database=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD
    )

    try:
        cur = conn.cursor()
        
    # Create ENUM types if they don't exist
        cur.execute("""
            DO $$
            BEGIN
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'job_type') THEN
                    CREATE TYPE job_type AS ENUM ('premium', 'normal');
                END IF;
                
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'industry_type') THEN
                    CREATE TYPE industry_type AS ENUM (
                        'Government',
                        'Banking & Financial Services',
                        'Fashion',
                        'Mining',
                        'Healthcare',
                        'IT - Software Development',
                        'IT - Data Analytics',
                        'IT - Cybersecurity',
                        'IT - Cloud Computing',
                        'IT - Artificial Intelligence',
                        'Agriculture',
                        'Automotive',
                        'Construction',
                        'Education',
                        'Energy & Utilities',
                        'Entertainment',
                        'Hospitality & Tourism',
                        'Legal',
                        'Manufacturing',
                        'Marketing & Advertising',
                        'Media & Communications',
                        'Non-Profit & NGO',
                        'Pharmaceuticals',
                        'Real Estate',
                        'Retail & Consumer Goods',
                        'Telecommunications',
                        'Transportation & Logistics'
                    );
                END IF;
                
                IF NOT EXISTS (SELECT 1 FROM pg_type WHERE typname = 'salary_range_type') THEN
                    CREATE TYPE salary_range_type AS ENUM (
                        '20000 - 40000',
                        '40000 - 60000',
                        '60000 - 80000',
                        '80000 - 100000',
                        '100000 - 120000',
                        '120000 - 140000',
                        '140000 - 160000',
                        '160000 - 180000',
                        '180000 - 200000',
                        '200000 - 220000',
                        '220000 - 240000',
                        '240000 - 260000',
                        '260000+'
                    );
                END IF;
            END $$;
        """)

        # Check for SEEKERS table:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'seekers'
            )
        """)
        table_exists = cur.fetchone()[0]

        # note: I created the state_enum and country_enum inside the db manually directly but have not added it here. Would need to:
        if not table_exists:
            cur.execute("""
                CREATE TABLE seekers (
                uid SERIAL PRIMARY KEY,
                first_name VARCHAR(255) NOT NULL,
                last_name VARCHAR(255) NOT NULL,
                email VARCHAR(255) UNIQUE NOT NULL,
                city VARCHAR(255) NOT NULL,
                state state_enum NOT NULL,
                country country_enum NOT NULL,
                datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);
            """)

        # Check for COMPANIES table:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'companies'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE companies (
                    company_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    city VARCHAR(255),
                    state VARCHAR(255),
                    country VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)
        
        # Check for RECRUITERS table
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'recruiters'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE recruiters (
                    recruiter_id SERIAL PRIMARY KEY,
                    company_id INTEGER,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    city VARCHAR(255),
                    state VARCHAR(255),
                    country VARCHAR(255),
                    is_direct_recruiter BOOLEAN,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (company_id)
                )
            """)

        # Check for JOBS table:
    # Check for JOBS table:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'jobs'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
            CREATE TABLE IF NOT EXISTS jobs (
                job_id SERIAL PRIMARY KEY,
                recruiter_id INTEGER,
                company_id INTEGER,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                specialization VARCHAR(255),
                job_type job_type NOT NULL DEFAULT 'normal',
                industry industry_type NOT NULL,
                salary_range salary_range_type,
                salary_type VARCHAR(10) CHECK (salary_type IN ('Annual', 'Hourly')),
                work_location VARCHAR(20) CHECK (work_location IN ('Office', 'Remote', 'Hybrid')),
                min_experience_years INTEGER,
                experience_level VARCHAR(50) CHECK (experience_level IN ('Entry Level', 'Associate', 'Mid-Senior Level', 'Director', 'Executive')),
                tech_stack TEXT[],
                city VARCHAR(255),
                state VARCHAR(255),
                country VARCHAR(255),
                expiry_date DATE DEFAULT CURRENT_DATE + INTERVAL '30 days',
                jobpost_url VARCHAR(255),
                work_rights TEXT[],
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recruiter_id) REFERENCES recruiters (recruiter_id),
                FOREIGN KEY (company_id) REFERENCES companies (company_id)
            )
        """)
        
        # Check for APPLICATIONS table:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'applications'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE applications (
                    applicationid SERIAL PRIMARY KEY,
                    userid INTEGER NOT NULL,
                    jobid INTEGER NOT NULL,
                    datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (userid) REFERENCES seekers (uid),
                    FOREIGN KEY (jobid) REFERENCES jobs (job_id)
                )
            """)

        # Check for BOOKMARKS table:
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'bookmarks'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE bookmarks (
                    bookmarksid SERIAL PRIMARY KEY,
                    userid INTEGER NOT NULL,
                    jobid INTEGER NOT NULL,
                    datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (userid) REFERENCES seekers (uid),
                    FOREIGN KEY (jobid) REFERENCES jobs (job_id)
                )
            """)

        conn.commit()
        print("Tables created successfully!")
        
    except psycopg2.Error as e:
        conn.rollback()
        print(f"Error creating tables: {e}")

    finally:
        cur.close()
        conn.close()