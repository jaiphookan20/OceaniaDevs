from database import PostgresDB

class RecruiterService:
    def __init__(self):
        self.db = PostgresDB()

    # Add a Job Post to the Jobs table
    def add_job(self, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights):
        query = """
            INSERT INTO jobs (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)
        self.db.execute_query(query, values)

    # Update Job Post (that is already present):
    # def update_job(self, job_id, updates):
    #     """
    #     Update a job post with given updates.
    #     :param job_id: int - The ID of the job to be updated.
       
    #     """
        
        
    #     self.db.execute_query(query, values)

    # Add a new Recruiter to the Recruiters table
    def add_recruiter(self, company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter):
        query = """
            INSERT INTO recruiters (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)
        self.db.execute_query(query, values)

    # Add a new Company to the Companies table
    def add_company(self, name, city, state, country):
        query = """
            INSERT INTO companies (name, city, state, country)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, city, state, country)
        self.db.execute_query(query, values)
