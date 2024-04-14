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
    
    def get_recruiters(self):
        query = """
            SELECT recruiter_id, first_name, last_name FROM recruiters
        """
        return self.db.fetch_data(query)

    def get_companies(self):
        query = """
            SELECT company_id, name FROM companies
        """
        return self.db.fetch_data(query)

    def populate_job_feed(self, uid, pagination_key, offset):
        # Implement the logic to populate the job feed based on user preferences
        pass

    def bookmark_a_job(self, uid, job_id, timestamp):
        # Implement the logic to bookmark a job for a user
        pass

    def marked_job_as_applied(self, uid, job_id, timestamp):
        # Implement the logic to mark a job as applied by a user
        pass