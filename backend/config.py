import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.environ.get('DB_HOST', 'postgres')  # Use 'postgres' as the default value
DB_HOST = os.getenv('DB_HOST', 'localhost')
DB_NAME = os.getenv('DB_NAME', 'job_board')
DB_USER = os.getenv('DB_USER', 'jai')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'techboard')
SECRET_KEY = os.getenv('SECRET_KEY', '1234567890')

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_SECRET_KEY=os.getenv('APP_SECRET_KEY')

# Test database configuration
TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'test_job_board')
TEST_DB_USER = os.getenv('TEST_DB_USER', 'jai')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'techboard')