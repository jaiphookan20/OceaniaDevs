from flask import Flask
from extensions import db
from models import *  # Import all models
from scraper_manager import process_scraped_data
import logging

# Set up basic logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

def create_app():
    app = Flask(__name__)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://dbmasteruser:techboard2024@ls-53acb3c0cb2cbe377b5ed78db92fdda1f3db8916.cfe6mimu8bzz.ap-southeast-2.rds.amazonaws.com:5432/Staging-Database'
    db.init_app(app)
    return app

if __name__ == '__main__':
    logger.info("Starting the scraper process")
    app = create_app()
    with app.app_context():
        logger.info("Processing scraped data")
        process_scraped_data()
    logger.info("Scraper process completed")
