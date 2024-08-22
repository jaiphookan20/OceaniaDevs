import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

DB_HOST = os.environ.get('DB_HOST', 'postgres')  # Use 'postgres' as the default value
# DB_HOST = os.getenv('DB_HOST', 'localhost') # use localhost, when using in local system, use 'postgres' when using in docker container
DB_NAME = os.getenv('DB_NAME', 'job_board')
DB_USER = os.getenv('DB_USER', 'jai')
DB_PASSWORD = os.getenv('DB_PASSWORD', 'techboard')
SECRET_KEY = os.getenv('SECRET_KEY', '1234567890')

AUTH0_CLIENT_ID = os.getenv('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.getenv('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.getenv('AUTH0_DOMAIN')
AUTH0_SECRET_KEY=os.getenv('APP_SECRET_KEY')

print(f"Loaded AUTH0_DOMAIN: {AUTH0_DOMAIN}")
print(f"Loaded AUTH0_CLIENT_ID: {AUTH0_CLIENT_ID}")
print(f"AUTH0_CLIENT_SECRET is set: {'Yes' if AUTH0_CLIENT_SECRET else 'No'}")
print(f"AUTH0_SECRET_KEY is set: {'Yes' if AUTH0_SECRET_KEY else 'No'}")

# Test database configuration
TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'test_job_board')
TEST_DB_USER = os.getenv('TEST_DB_USER', 'jai')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'techboard')

BASE_URL = os.getenv('BASE_URL', 'http://54.79.190.69')

# Uncomment and use http://localhost during local docker setup ie not in AWS Lightsail
# BASE_URL = os.getenv('BASE_URL', 'http://localhost') 
