import os
import sys
from pathlib import Path
from apify_client import ApifyClient
from typing import List, Dict, Any, Tuple
from flask import Flask, current_app
from dotenv import load_dotenv
import logging
import json
from PIL import Image
import io
import requests
from werkzeug.utils import secure_filename

# Get the absolute path to the backend directory
current_dir = Path(__file__).resolve().parent
backend_dir = current_dir.parent

# Add the backend directory to Python's path
sys.path.append(str(backend_dir))

# Now import your modules
from app import create_app
from service.recruiter_service import RecruiterService
from models import Company, db, Job
from sqlalchemy.exc import SQLAlchemyError

load_dotenv()

# Set up logging configuration
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.StreamHandler(),
    ]
)
logger = logging.getLogger(__name__)

# Define constants for output directories
LOGO_UPLOAD_DIR = 'uploads/upload_company_logo'

# Create Flask app
app = create_app()
app.logger.setLevel(logging.INFO)

# Update database configuration if needed
if os.environ.get('STAGING_DB_HOST'):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ.get("STAGING_DB_USER")}:{os.environ.get("STAGING_DB_PASSWORD")}@{os.environ.get("STAGING_DB_HOST")}:{os.environ.get("STAGING_DB_PORT")}/Staging-Database'

# Initialize the ApifyClient with API token
client = ApifyClient(os.environ["APIFY_API_KEY"])

def get_existing_job_urls():
    """Get all existing jobpost_urls from the Jobs table"""
    try:
        existing_urls = db.session.query(Job.jobpost_url).all()
        return {url[0] for url in existing_urls if url[0]}  # Convert to set for O(1) lookup
    except SQLAlchemyError as e:
        logger.error(f"Error fetching existing job URLs: {e}")
        return set()

def get_or_create_company(company_name: str, logo_url=None):
    """Get an existing company or create a new one if it doesn't exist.
    
    Args:
        company_name (str): Name of the company
        logo_url (str, optional): URL of the company logo
    
    Returns:
        Company: The company object from the database
        
    Raises:
        SQLAlchemyError: If there is a database error
        ValueError: If company_name is empty or invalid
    """
    try:
        with db.session.begin_nested():
            company = Company.query.filter_by(name=company_name).first()
            if not company:
                logger.info(f"Creating new company: {company_name}")
                company = Company(name=company_name)
                db.session.add(company)
                
                # CHANGE: Process logo inside transaction if new company
                if logo_url:
                    download_and_save_logo(company, logo_url)
                    
                db.session.flush()  # Flush to get the company ID
                logger.info(f"Successfully created company with ID: {company.company_id}")
            else:
                logger.info(f"Found existing company: {company_name}")
                    
            return company
            
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting/creating company {company_name}: {str(e)}")
        db.session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error while getting/creating company {company_name}: {str(e)}")
        db.session.rollback()
        raise

def download_and_save_logo(company, logo_url):
    try:
        response = requests.get(logo_url)
        if response.status_code == 200:
            image = Image.open(io.BytesIO(response.content))
            
            # Convert to RGB if the image is in RGBA mode
            if image.mode == 'RGBA':
                image = image.convert('RGB')
            
            # Resize the image to 400x400 while maintaining aspect ratio
            image.thumbnail((400, 400))
            
            # Create a new white background image
            background = Image.new('RGB', (400, 400), (255, 255, 255))
            
            # Calculate position to paste the resized image
            paste_position = ((400 - image.width) // 2, (400 - image.height) // 2)
            
            # Paste the resized image onto the white background
            background.paste(image, paste_position)
            
            filename = secure_filename(f"{company.company_id}_{os.path.basename(logo_url)}")
            logo_path = os.path.join(LOGO_UPLOAD_DIR, filename)
            
            os.makedirs(os.path.dirname(logo_path), exist_ok=True)
            
            # Save as WebP format
            background.save(logo_path, 'WEBP', quality=85)
            
            company.logo_url = f"{app.config.BASE_URL}/uploads/upload_company_logo/{filename}"
    except Exception as e:
        logger.error(f"Error downloading logo for {company.name}: {str(e)}")

def run_scraper(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run the Actor and wait for it to finish, saving results to JSON file"""
    run = client.actor("racH8InrI6hwjhzCc").call(run_input=input_data)
    items = list(client.dataset(run["defaultDatasetId"]).iterate_items())

    processed_items = []
    for item in items:
        # Get company name from item or advertiser description
        company_name = item.get('companyName') or ""
        
        # Get logo URL with fallback logic
        logo_url = ""
        if (item.get('branding') and item.get('branding').get('assets') and 
            item.get('branding').get('assets').get('logo') and 
            item.get('branding').get('assets').get('logo').get('strategies')):
            strategies = item['branding']['assets']['logo']['strategies']
            logo_url = strategies.get('jdpLogo') or strategies.get('serpLogo') or ""

        # Get work arrangements
        work_arrangements = ""
        if item.get('workArrangements') and item.get('workArrangements').get('data'):
            arrangements = []
            for arr in item['workArrangements']['data']:
                if arr.get('label') and arr.get('label').get('text'):
                    arrangements.append(arr['label']['text'])
            work_arrangements = ", ".join(arrangements)

        processed_item = {
            'company': company_name,
            'companyLogo': logo_url,
            'location': item.get('location'),
            'title': item.get('title'),
            'description': '\n'.join(filter(None, [
                item.get('content', ''),
                f"Teaser: {item.get('teaser', '')}" if item.get('teaser') else '',
                'Bullet Points:' if item.get('bulletPoints') else '',
                '\n'.join(f"• {point}" for point in item.get('bulletPoints', [])) if item.get('bulletPoints') else '',
                f"Work Arrangements: {work_arrangements}" if work_arrangements else '',
                f"Salary: {item.get('salary', '')}" if item.get('salary') else ''
            ])),
            'url': item.get('url'),
        }
        processed_items.append(processed_item)
    
    return processed_items

def process_results(items: List[Dict[str, Any]]) -> Tuple[int, List[str]]:
    recruiter_service = RecruiterService()
    stats = {
        'total_scraped': 0,
        'skipped_existing': 0,
        'skipped_non_australia': 0,      
        'skipped_department': 0,
        'successfully_added': 0,
        'failed': 0
    }
    errors = []
    
    try:
        # Get all existing job URLs
        existing_urls = get_existing_job_urls()
        logger.info(f"Found {len(existing_urls)} existing jobs in database")

        stats['total_scraped'] = len(items)
        
        for job in items:
            try:
                # Check if job URL already exists
                job_url = job.get('url')
                if not job_url:
                    stats['failed'] += 1
                    errors.append(f"Missing URL for job: {job.get('title', 'Unknown')}")
                    continue

                if job_url in existing_urls:
                    stats['skipped_existing'] += 1
                    logger.info(f"Skipping existing job: {job.get('title')} ({job_url})")
                    continue

                # Get or create company
                company_name = job.get('companyName') or job.get('advertiser', {}).get('description', '')
                company_obj = get_or_create_company(company_name)
                
                if not company_obj:
                    stats['failed'] += 1
                    errors.append(f"Failed to create/get company for job: {job.get('title')}")
                    continue

                # Prepare job details
                job_details = {
                    'recruiter_id': 1,  # Admin recruiter ID
                    'company_id': company_obj.company_id,
                    'title': job.get('title'),
                    'jobpost_url': job_url,
                    'city': job.get('location'),
                    'country': 'Australia',
                    'description': job.get('description'),
                }

                # Add job using recruiter service
                new_job, error = recruiter_service.add_job_programmatically_admin(job_details)
                
                if error:
                    stats['failed'] += 1
                    errors.append(f"Error adding job {job.get('title')}: {error}")
                    logger.error(f"Failed to add job: {error}")
                    continue

                # Verify the job was actually created
                created_job = Job.query.get(new_job.job_id)
                if not created_job:
                    stats['failed'] += 1
                    error_msg = f"Job with ID {new_job.job_id} not found after creation"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    continue

                # Explicitly commit after each successful job addition
                try:
                    db.session.commit()
                    stats['successfully_added'] += 1
                    logger.info(f"Successfully added and verified job: {job.get('title')} with ID {created_job.job_id}")
                except SQLAlchemyError as e:
                    db.session.rollback()
                    stats['failed'] += 1
                    error_msg = f"Database commit failed for job {job.get('title')}: {str(e)}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    continue

            except Exception as error:
                stats['failed'] += 1
                error_msg = f"Error processing job {job.get('title', 'Unknown')}: {str(error)}"
                errors.append(error_msg)
                logger.error(error_msg)
                continue

        # Log final statistics
        logger.info("\n=== Job Processing Statistics ===")
        logger.info(f"Total jobs scraped: {stats['total_scraped']}")
        logger.info(f"Jobs skipped (already exist): {stats['skipped_existing']}")
        logger.info(f"Jobs skipped (non-Australian): {stats['skipped_non_australia']}")
        logger.info(f"Jobs successfully added: {stats['successfully_added']}")
        logger.info(f"Jobs failed to add: {stats['failed']}")
        logger.info(f"Total errors encountered: {len(errors)}")
        logger.info("=============================\n")

        return stats['successfully_added'], errors

    except Exception as e:
        db.session.rollback()
        error_msg = f"Fatal error in process_results: {str(e)}"
        logger.error(error_msg, exc_info=True)
        return 0, [error_msg]


# Usage
if __name__ == "__main__":
    with app.app_context():  # This is the key addition
        input_data = {
    "category": [
        "6281"
    ],
    "country": "australia",
    "days": 1,
    "dev_dataset_clear": False,
    "dev_no_strip": False,
    "sort": "date",
    "types.casual": False,
    "types.contract": False,
    "types.full": False,
    "types.part": False,
    "limit": 10,
    }
 
        try:
            logger.info("Starting job scraping process...")  # Changed from current_app.logger
            results = run_scraper(input_data)
            successful_adds, errors = process_results(results)
            
            logger.info(f"Scraping process completed.")  # Changed from current_app.logger
            logger.info(f"Successfully added {successful_adds} new jobs to the database.")
            
            if errors:
                logger.warning(f"Encountered {len(errors)} errors during processing:")
                for error in errors:
                    logger.warning(error)
        except Exception as e:
            logger.error(f"Fatal error during scraping: {str(e)}", exc_info=True)

