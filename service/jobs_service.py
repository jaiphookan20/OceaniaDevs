from database import PostgresDB

class JobsService:
    def __init__(self):
        self.db = PostgresDB()

    # Retrieve a job post by its ID
    def get_job_by_id(self, job_id):
        """
        Retrieve a job post by its ID.
        :param job_id: int - The ID of the job to fetch.
        :return: job details as a dictionary
        """
        query = """
            SELECT * FROM jobs WHERE job_id = %s;
        """
        return self.db.fetch_one(query, (job_id,))
    
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
    
    # Return the list of all available jobs along with job title, company name, job city, state, country
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