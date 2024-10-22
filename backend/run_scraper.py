from flask import Flask
from extensions import db
from models import *  # Import all models
from scraper_manager import process_scraped_data
import logging
from dotenv import load_dotenv
load_dotenv()
# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

STAGING_DB_HOST = os.environ.get('STAGING_DB_HOST')
STAGING_DB_PORT = os.environ.get('STAGING_DB_PORT')
STAGING_DB_NAME = os.environ.get('STAGING_DB_NAME')
STAGING_DB_USER = os.environ.get('STAGING_DB_USER')
STAGING_DB_PASSWORD = os.environ.get('STAGING_DB_PASSWORD')

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{STAGING_DB_USER}:{STAGING_DB_PASSWORD}@{STAGING_DB_HOST}:{STAGING_DB_PORT}/Staging-Database'
    db.init_app(app)
    return app

if __name__ == '__main__':
    logger.info("Starting the scraper process")
    app = create_app()
    with app.app_context():
        logger.info("Processing scraped data")
        process_scraped_data()
    logger.info("Scraper process completed")
