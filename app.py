from flask import Flask
from db import PostgresDB

# In the given code, app = Flask(__name__) creates an instance of the Flask class and assigns it to the variable app.
# The __name__ argument is a special Python variable that represents the name of the current module in which the code is executed. By passing __name__ as the argument to Flask(), you are telling Flask to use the current module as the basis for finding resources such as templates and static files.

app = Flask(__name__)  # references this file


@app.route('/')
def index():
    db = PostgresDB()
    db.connect()
    return "Hello, World!"
