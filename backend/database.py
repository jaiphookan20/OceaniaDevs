import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD

class PostgresDB:
    def __init__(self):
        self.conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )

    def execute_query(self, query, values=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, values)
            self.conn.commit()
            cur.close()
        except psycopg2.Error as e:
            print(f"Error executing query: {e}")
            self.conn.rollback()

    def fetch_data(self, query, values=None):
        try:
            cur = self.conn.cursor()
            cur.execute(query, values)
            data = cur.fetchall()
            cur.close()
            return data
        except psycopg2.Error as e:
            print(f"Error fetching data: {e}")
            return None

    def close_connection(self):
        self.conn.close()