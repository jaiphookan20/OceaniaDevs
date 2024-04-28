from database import PostgresDB

class SeekerService:
    def __init__(self):
        self.db = PostgresDB()

    def add_seeker(self, first_name, last_name, email, city, state, country):
        query = """
            INSERT INTO seekers (first_name, last_name, email, city, state, country)
            VALUES (%s, %s, %s, %s, %s, %s)
        """
        values = (first_name, last_name, email, city, state, country)
        self.db.execute_query(query, values)