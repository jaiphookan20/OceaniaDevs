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
from PIL import Image
import io

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
    """
    Process scraped job data from various sources and archive the input files.

    This function iterates through predefined sources (currently only 'seek'),
    processes the scraped job data, and archives the input files with a timestamp.
    """
    logger.info("Starting process_scraped_data function")
    
    # Generate current date string for archiving
    date_str = datetime.now().strftime('%d-%m-%Y')
    
    # Iterate through each source (currently only 'seek')
    for source in ['seek']:
        # Define input and archive file paths
        input_file = os.path.join(SCRAPER_OUTPUT_DIR, f'{source}.json')
        archive_file = os.path.join(ARCHIVE_DIR, f"{source}_{date_str}.json")
        
        logger.info(f"Checking for input file: {input_file}")
        
        # Check if the input file exists
        if os.path.exists(input_file):
            logger.info(f"Processing jobs from {input_file}")
            # Process jobs from the input file
            process_jobs_from_file(input_file, source)
            
            logger.info(f"Archiving file to {archive_file}")
            # Ensure the archive directory exists
            os.makedirs(os.path.dirname(archive_file), exist_ok=True)
            # Move the processed file to the archive
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
    Use Perplexity API to fill in missing details.
    
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
            
            # Use Perplexity API to get company details
            company_details = get_company_details_from_perplexity(company_name)
            
            # Update company fields with the retrieved information
            company.description = company_details.get('description', '')
            company.city = company_details.get('city', '')
            company.state = company_details.get('state', '')
            company.industry = company_details.get('industry', '')
    
    if logo_url:
        download_and_save_logo(company, logo_url)
    
    return company

def get_company_details_from_perplexity(company_name):
    """
    Use Perplexity API to get company details.
    
    Args:
    company_name (str): Name of the company
    
    Returns:
    dict: Company details including description, city, state, and industry
    """
    api_key = current_app.config['PERPLEXITY_API_KEY']
    logger.info(f"PERPLEXITY_API_KEY: {api_key}")
    url = "https://api.perplexity.ai/chat/completions"
    
    # CHANGE: Updated prompt to be more specific and request JSON output
    prompt = f"""Provide details for the company '{company_name}', based in Australia, in JSON format with the following keys:
    1. 'description': A short blurb (max 200 characters) about the company and its activities.
    2. 'city': The city of the company's headquarters in Australia. Choose from: Sydney, Melbourne, Brisbane, Perth, Adelaide, Gold Coast, Newcastle, Canberra, Geelong, Hobart, Townsville, Cairns, Darwin. You cannot provide a city that is not in the list.
    3. 'state': The state of the company's headquarters in Australia. Choose from: VIC, NSW, ACT, WA, QLD, NT, TAS, SA. You cannot provide a state that is not in the list.
    4. 'industry': The primary industry of the company. Choose only one from: Government, Banking & Financial Services, Fashion, Mining, Healthcare, IT - Software Development, IT - Data Analytics, IT - Cybersecurity, IT - Cloud Computing, IT - Artificial Intelligence, Agriculture, Automotive, Construction, Education, Energy & Utilities, Entertainment, Hospitality & Tourism, Legal, Manufacturing, Marketing & Advertising, Media & Communications, Non-Profit & NGO, Pharmaceuticals, Real Estate, Retail & Consumer Goods, Telecommunications, Transportation & Logistics. You cannot provide an industry that is not in the list.
    
    Strictly provide ONLY the JSON output, no additional text."""
    
    payload = {
        "model": "llama-3.1-sonar-small-128k-online",
        "messages": [
            {
                "role": "system",
                "content": "You are a helpful assistant that provides accurate company information in JSON format."
            },
            {
                "role": "user",
                "content": prompt
            }
        ],
        "max_tokens": 500,
        "temperature": 0.2,
        "top_p": 0.9,
        "stream": False
    }

    headers = {
        "accept": "application/json",
        "content-type": "application/json",
        "authorization": f"Bearer {api_key}"
    }
    
    try:
        response = requests.post(url, json=payload, headers=headers)
        response.raise_for_status()
        result = response.json()
        # CHANGE: Directly parse the JSON from the content
        company_details = json.loads(result['choices'][0]['message']['content'])
        return company_details
    except Exception as e:
        logger.error(f"Error fetching company details from Perplexity API: {str(e)}")
        return {}

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
            
            company.logo_url = f"{config.BASE_URL}/uploads/upload_company_logo/{filename}"
    except Exception as e:
        logger.error(f"Error downloading logo for {company.name}: {str(e)}")

if __name__ == '__main__':
    process_scraped_data()
