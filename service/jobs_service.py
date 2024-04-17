from database import PostgresDB

class JobsService:
    def __init__(self):
        self.db = PostgresDB()

    def add_job(self, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights):
        query = """
            INSERT INTO jobs (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)
        self.db.execute_query(query, values)
    
    # Return the list of all Recruiters
    def get_recruiters(self):
        query = """
            SELECT recruiter_id, first_name, last_name FROM recruiters
        """
        return self.db.fetch_data(query)

    # Return the list of all Companies
    def get_companies(self):
        query = """
            SELECT company_id, name FROM companies
        """
        return self.db.fetch_data(query)
    
    def get_available_jobs(self):
        query = """
            SELECT j.job_id, j.title, c.name AS company_name, j.city, j.state, j.country
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
        """
        return self.db.fetch_data(query)
    
    # Apply to a particular job post
    def apply_to_job(self, userid, jobid):
        query = """
            INSERT INTO applications (userid, jobid)
            VALUES (%s, %s)
        """
        values = (userid, jobid)
        self.db.execute_query(query, values)

    # Bookmark a particular job post
    def bookmark_job(self, userid, jobid):
        query = """
            INSERT INTO bookmarks (userid, jobid)
            VALUES (%s, %s)
        """
        values = (userid, jobid)
        self.db.execute_query(query, values)

    # Filter jobs based on
    def filter_jobs(self, company_id=None, experience_level=None, industry=None):
        query = """
            SELECT j.job_id, j.title, c.name AS company_name, j.city, j.state, j.country
            FROM jobs j
            JOIN companies c ON j.company_id = c.company_id
            WHERE 1=1
        """
        params = []
        
        if company_id:
            query += " AND j.company_id = %s"
            params.append(company_id)
        
        if experience_level:
            query += " AND j.experience_level = %s"
            params.append(experience_level)
        
        if industry:
            query += " AND j.industry = %s"
            params.append(industry)
        
        return self.db.fetch_data(query, params)

    def populate_job_feed(self, uid, pagination_key, offset):
        # Implement the logic to populate the job feed based on user preferences
        pass