from database import PostgresDB

class RecruiterService:
    def __init__(self):
        self.db = PostgresDB()

    def add_recruiter(self, company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter):
        query = """
            INSERT INTO recruiters (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)
        self.db.execute_query(query, values)

    
    def add_company(self, name, city, state, country):
        query = """
            INSERT INTO companies (name, city, state, country)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, city, state, country)
        self.db.execute_query(query, values)
