import os
from dotenv import load_dotenv

load_dotenv()

DB_HOST = os.environ.get('DB_HOST', 'postgres')
DB_NAME = os.environ.get('DB_NAME')
DB_USER = os.environ.get('DB_USER')
DB_PASSWORD = os.environ.get('DB_PASSWORD')
SECRET_KEY = os.environ.get('SECRET_KEY')

LIGHTSAIL_DB_HOST = os.environ.get('LIGHTSAIL_DB_HOST')
LIGHTSAIL_DB_PORT = os.environ.get('LIGHTSAIL_DB_PORT')
LIGHTSAIL_DB_NAME = os.environ.get('LIGHTSAIL_DB_NAME')
LIGHTSAIL_DB_USER = os.environ.get('LIGHTSAIL_DB_USER')
LIGHTSAIL_DB_PASSWORD = os.environ.get('LIGHTSAIL_DB_PASSWORD')

STAGING_DB_HOST = os.environ.get('STAGING_DB_HOST')
STAGING_DB_PORT = os.environ.get('STAGING_DB_PORT')
STAGING_DB_NAME = os.environ.get('STAGING_DB_NAME')
STAGING_DB_USER = os.environ.get('STAGING_DB_USER')
STAGING_DB_PASSWORD = os.environ.get('STAGING_DB_PASSWORD')

AUTH0_CLIENT_ID = os.environ.get('AUTH0_CLIENT_ID')
AUTH0_CLIENT_SECRET = os.environ.get('AUTH0_CLIENT_SECRET')
AUTH0_DOMAIN = os.environ.get('AUTH0_DOMAIN')
AUTH0_SECRET_KEY = os.environ.get('APP_SECRET_KEY')

MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 587
MAIL_USE_TLS = True
MAIL_USERNAME = os.environ.get('MAIL_USERNAME')
MAIL_PASSWORD = os.environ.get('MAIL_PASSWORD')
MAIL_DEFAULT_SENDER = os.environ.get('MAIL_DEFAULT_SENDER')

PERPLEXITY_API_KEY = os.environ.get('PERPLEXITY_API_KEY')

# print(f"DB_HOST: {DB_HOST}")
# print(f"DB_NAME: {DB_NAME}")
# print(f"DB_USER: {DB_USER}")
# print(f"DB_PASSWORD is set: {'Yes' if DB_PASSWORD else 'No'}")
# print(f"Loaded AUTH0_DOMAIN: {AUTH0_DOMAIN}")
# print(f"Loaded AUTH0_CLIENT_ID: {AUTH0_CLIENT_ID}")
# print(f"AUTH0_CLIENT_SECRET is set: {'Yes' if AUTH0_CLIENT_SECRET else 'No'}")
# print(f"AUTH0_SECRET_KEY is set: {'Yes' if AUTH0_SECRET_KEY else 'No'}")

# Test database configuration
TEST_DB_NAME = os.getenv('TEST_DB_NAME', 'test_job_board')
TEST_DB_USER = os.getenv('TEST_DB_USER', 'jai')
TEST_DB_PASSWORD = os.getenv('TEST_DB_PASSWORD', 'techboard')

BASE_URL = os.getenv('BASE_URL', 'http://54.79.190.69')
# Uncomment and use http://localhost during local docker setup ie not in AWS Lightsail
# BASE_URL = os.getenv('BASE_URL', 'http://localhost') 
