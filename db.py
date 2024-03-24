# import os
# import psycopg2


# data = {

#     "fname": "aaditya",
#     "lname": "menon",
#     "city": "Mumbai",
#     "state": "MH",
#     "country": "India",
#     "email": ""
# }

# filters_and = {

#     "fname": "aaditya",
#     "lname": "menon",
# }

# filters_or = {

#     "fname": "aaditya",
#     "lname": "menon",
# }


# class PostgresDB:
#     def init_db(self):
#         pass

#     def connect(self):
#         conn = psycopg2.connect(
#             host="localhost",
#             database="flask_db",
#             user='aadityamenon',
#             password='')  # empty

#         cur = conn.cursor()

#         cur.execute('SELECT * FROM seekers;')
#         rows = cur.fetchall()
#         print(rows)
#         cur.execute(f"""INSERT INTO seekers (fname, lname, city, state, country, email, work_auth) 
# VALUES (%s, %s, %s, %s, %s, %s, %s)""", ("gary", "w", "Mumbai", "MH", "India", "gary@gmail.com", "aus_work_visa"))
#         conn.commit()
#         cur.close()
#         conn.close()

#     def insert_into_table(self, table_name, data: dict):
#         # rawl sql --> sqlalchemy
#         pass

#     def select_from_table(self, table_name, filters: dict):
#         pass
