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
    
    # Need to add in for Seekers as well
    # CREATE TABLE seekers (
    # uid SERIAL PRIMARY KEY,
    # fname VARCHAR(255) NOT NULL,
    # lname VARCHAR(255) NOT NULL,
    # city VARCHAR(255) NOT NULL,
    # state state_enum NOT NULL,
    # country country_enum NOT NULL,
    # email_id VARCHAR(255) UNIQUE NOT NULL,
    # datetimestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP);

        # Check if the companies table exists, and create it if it doesn't
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
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        # Check if the jobs table exists, and create it if it doesn't
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
                agent_id INTEGER,
                company_id INTEGER,
                agency_id INTEGER,
                title VARCHAR(255) NOT NULL,
                description TEXT,
                specialization VARCHAR(255),
                job_type VARCHAR(20) CHECK (job_type IN ('Contract', 'Part-Time', 'Casual', 'Full-Time', 'Internship')),
                salary_range VARCHAR(50),
                salary_type VARCHAR(10) CHECK (salary_type IN ('Annual', 'Hourly')),
                work_location VARCHAR(20) CHECK (work_location IN ('Office', 'Remote', 'Hybrid')),
                experience_years VARCHAR(50),
                experience_level VARCHAR(50) CHECK (experience_level IN ('Entry Level', 'Associate', 'Mid-Senior Level', 'Director', 'Executive')),
                industry VARCHAR(255),
                tech_stack TEXT[],
                city VARCHAR(255),
                state VARCHAR(255),
                country VARCHAR(255),
                expiry_date DATE,
                jobpost_url VARCHAR(255),
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (recruiter_id) REFERENCES recruiters (recruiter_id),
                FOREIGN KEY (agent_id) REFERENCES agents (agent_id),
                FOREIGN KEY (company_id) REFERENCES companies (company_id),
                FOREIGN KEY (agency_id) REFERENCES agencies (agency_id)
            )
        """)

        # Check if the recruiters table exists, and create it if it doesn't
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
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (company_id) REFERENCES companies (company_id)
                )
            """)

        # Check if the agencies table exists, and create it if it doesn't
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'agencies'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE agencies (
                    agency_id SERIAL PRIMARY KEY,
                    name VARCHAR(255) NOT NULL,
                    location VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                )
            """)

        # Check if the agents table exists, and create it if it doesn't
        cur.execute("""
            SELECT EXISTS (
                SELECT FROM information_schema.tables
                WHERE table_schema = 'public' AND table_name = 'agents'
            )
        """)
        table_exists = cur.fetchone()[0]
        if not table_exists:
            cur.execute("""
                CREATE TABLE agents (
                    agent_id SERIAL PRIMARY KEY,
                    agency_id INTEGER,
                    first_name VARCHAR(255) NOT NULL,
                    last_name VARCHAR(255) NOT NULL,
                    email VARCHAR(255) NOT NULL,
                    password VARCHAR(255) NOT NULL,
                    city VARCHAR(255),
                    state VARCHAR(255),
                    country VARCHAR(255),
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (agency_id) REFERENCES agencies (agency_id)
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