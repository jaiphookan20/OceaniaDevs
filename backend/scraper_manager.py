# Import necessary modules
import subprocess
import os
import json
from datetime import datetime
from models import db, Company, Job
from service.recruiter_service import RecruiterService
import requests
from werkzeug.utils import secure_filename
import config
from celery import Celery
import logging
import sys
from sqlalchemy.exc import SQLAlchemyError
from flask import current_app
from extensions import db

# Set up logging
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(name)s - %(levelname)s - %(message)s')
logger = logging.getLogger(__name__)

# If you want to log to both console and file
file_handler = logging.FileHandler('scraper.log')
file_handler.setLevel(logging.INFO)
file_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

console_handler = logging.StreamHandler(sys.stdout)
console_handler.setLevel(logging.INFO)
console_handler.setFormatter(logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s'))

logger.addHandler(file_handler)
logger.addHandler(console_handler)

# Define constants for output directories
SCRAPER_OUTPUT_DIR = 'scraper_output'
ARCHIVE_DIR = 'scraper_archive'
LOGO_UPLOAD_DIR = 'uploads/upload_company_logo'

# Initialize Celery app
celery = Celery(__name__)
celery.conf.broker_url = os.environ.get("CELERY_BROKER_URL", "redis://localhost:6379")
celery.conf.result_backend = os.environ.get("CELERY_RESULT_BACKEND", "redis://localhost:6379")

@celery.task
def run_daily_job_processing():
    """
    Celery task to run daily job processing.
    This function orchestrates the scraping and processing of job data.
    """
    run_scrapers()
    process_scraped_data()

def run_scrapers():
    """
    Run all configured scrapers.
    Currently, only the Seek scraper is implemented.
    """
    run_seek_scraper()
    # Add other scrapers here in the future

def run_seek_scraper():
    """
    Execute the Seek scraper using a Node.js script.
    The scraped data is saved to a JSON file in the output directory.
    """
    # CHANGE: Updated the path to use the frontend directory
    # CHANGE: Ensure the SCRAPER_OUTPUT_DIR exists
    os.makedirs(SCRAPER_OUTPUT_DIR, exist_ok=True)
    output_file = os.path.join(SCRAPER_OUTPUT_DIR, 'seek.json')
    subprocess.run(['node', '../frontend/apify_seek_scraper.js', '--output', output_file], check=True)

def process_scraped_data():
    logger.info("Starting process_scraped_data function")
    date_str = datetime.now().strftime('%d-%m-%Y')
    
    for source in ['seek']:
        input_file = os.path.join(SCRAPER_OUTPUT_DIR, f'{source}.json')
        archive_file = os.path.join(ARCHIVE_DIR, f"{source}_{date_str}.json")
        
        logger.info(f"Checking for input file: {input_file}")
        if os.path.exists(input_file):
            logger.info(f"Processing jobs from {input_file}")
            process_jobs_from_file(input_file, source)
            
            logger.info(f"Archiving file to {archive_file}")
            os.makedirs(os.path.dirname(archive_file), exist_ok=True)
            os.rename(input_file, archive_file)
        else:
            logger.warning(f"Input file not found: {input_file}")
    
    logger.info("Finished process_scraped_data function")

def process_jobs_from_file(file_path, source):
    logger.info(f"Starting to process jobs from {file_path}")
    with open(file_path, 'r') as file:
        jobs_data = json.load(file)
    
    recruiter_service = RecruiterService()
    processed_jobs = 0
    errors = []

    for job_data in jobs_data:
        try:
            with db.session.begin():
                company = get_or_create_company(job_data['companyName'], job_data.get('companyLogo'))
                
                job_details = {
                    'recruiter_id': 1,  # Admin recruiter ID
                    'company_id': company.company_id,
                    'title': job_data['title'],
                    'jobpost_url': job_data['url'],
                    'city': job_data.get('location', ''),
                    'job_arrangement': job_data.get('workType', ''),
                    'country': 'Australia',
                    'description': job_data['description'],
                    'teaser': job_data.get('teaser', ''),
                    'salary': job_data.get('salary', ''),
                    'subClassification': job_data.get('subClassification', '')
                }
                
                new_job, error = recruiter_service.add_job_programmatically_admin(job_details)
                if error:
                    raise Exception(error)
                
                processed_jobs += 1
                logger.info(f"Successfully processed job: {job_data['title']}")
        except Exception as e:
            errors.append(f"Error processing job '{job_data.get('title', 'Unknown')}': {str(e)}")
            logger.error(f"Error processing job from {source}: {str(e)}", exc_info=True)
    
    logger.info(f"Finished processing jobs from {file_path}. Processed {processed_jobs} jobs with {len(errors)} errors.")
    return processed_jobs, errors

def get_or_create_company(company_name, logo_url=None):
    """
    Get an existing company or create a new one if it doesn't exist.
    
    Args:
    company_name (str): Name of the company
    logo_url (str, optional): URL of the company logo
    
    Returns:
    Company: The company object from the database
    """
    with db.session.begin_nested():
        company = Company.query.filter_by(name=company_name).first()
        if not company:
            company = Company(name=company_name)
            db.session.add(company)
    
    if logo_url:
        download_and_save_logo(company, logo_url)
    
    return company

def download_and_save_logo(company, logo_url):
    """
    Download and save a company logo.
    """
    try:
        # Send a GET request to download the logo
        response = requests.get(logo_url)
        if response.status_code == 200:
            # Generate a secure filename for the logo
            filename = secure_filename(f"{company.company_id}_{os.path.basename(logo_url)}")
            # Create the full path where the logo will be saved
            logo_path = os.path.join(LOGO_UPLOAD_DIR, filename)
            
            # Ensure the directory exists
            os.makedirs(os.path.dirname(logo_path), exist_ok=True)
            # Save the downloaded logo to the file system
            with open(logo_path, 'wb') as f:
                f.write(response.content)
            
            # Update the company's logo URL in the database
            company.logo_url = f"{config.BASE_URL}/uploads/upload_company_logo/{filename}"
    except Exception as e:
        # Log any errors that occur during the logo download process
        logger.error(f"Error downloading logo for {company.name}: {str(e)}")

if __name__ == '__main__':
    process_scraped_data()
