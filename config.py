import os
DB_HOST = os.environ.get('DB_HOST', 'localhost')
DB_NAME = os.environ.get('DB_NAME', 'job_board')
DB_USER = os.environ.get('DB_USER', 'jai')
DB_PASSWORD = os.environ.get('DB_PASSWORD', 'techboard')
SECRET_KEY="1234567890"

# # Test database configuration
# TEST_DB_NAME = os.environ.get('TEST_DB_NAME', 'test_job_board')
# TEST_DB_USER = os.environ.get('TEST_DB_USER', DB_USER)
# TEST_DB_PASSWORD = os.environ.get('TEST_DB_PASSWORD', DB_PASSWORD)

# Test database configuration
TEST_DB_NAME = os.environ.get('TEST_DB_NAME', 'test_job_board')
TEST_DB_USER = os.environ.get('TEST_DB_USER', 'jai')
TEST_DB_PASSWORD = os.environ.get('TEST_DB_PASSWORD', 'techboard')
