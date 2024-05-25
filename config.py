import os
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'job_board')
DB_USER = os.environ.get('DB_USER', 'jai')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'techboard')
SECRET_KEY="1234567890"