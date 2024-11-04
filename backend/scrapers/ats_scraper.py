import os
import sys
from pathlib import Path
from apify_client import ApifyClient
from typing import List, Dict, Any, Tuple
from flask import Flask, current_app
from dotenv import load_dotenv
import logging
import json
from celery_app import celery  # Import the celery instance directly
from utils.email_utils import send_scraper_report

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

# Create Flask app
app = create_app()
app.logger.setLevel(logging.INFO)

# Update database configuration if needed
if os.environ.get('STAGING_DB_HOST'):
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{os.environ.get("STAGING_DB_USER")}:{os.environ.get("STAGING_DB_PASSWORD")}@{os.environ.get("STAGING_DB_HOST")}:{os.environ.get("STAGING_DB_PORT")}/Staging-Database'

# Initialize the ApifyClient with API token
client = ApifyClient(os.environ["APIFY_API_KEY"])

# Company departments configuration
company_departments = {
    # "aulogicalis": ["Managed Services (MS)"],
    # "auspayplus": ["Technology"],
    # "ofload": ["Technology"],
    # "datacom1": ["Technology", "Infrastructure Products"],
    "compass-education": ["Product"],
    "buildkite": ["Engineering"],
    "immutable": ["Platform | Security & IT"],
    "octoenergy": ["Software Engineering"],
    "xero": ["Engineering", "Product", "Reliability"],
    "recordpoint": ["Application Engineering"],
    "myob": ["Software Development"],
    "blinq": ["Engineering"],
    "octopus": ["110 - Engineering"],
    "Zeller": ["Devices and Frontend", "Cloud & Security"],
    "swyftx": ["Engineering"],
    "carsales": ["Data Platform and Engineering", "Technology - Retail", "iMotor"],

}

# Add this near the top with other configurations
company_name_mapping = {
    # Workable companies
    "datacom1": "Datacom",
    "archipro-3": "ArchiPro",
    "auspayplus": "AusPay Plus",
    "demystdata": "Demyst",
    "aulogicalis": "Logicalis Australia",
    "ofload": "Ofload",
    "compass-education": "Compass Education",

    # Lever companies
    "octoenergy": "Octopus Energy",
    "xero": "Xero",
    "recordpoint": "RecordPoint",
    "myob": "MYOB",
    "blinq": "Blinq",
    "octopus": "Octopus Deploy",
    "Zeller": "Zeller",
    "swyftx": "Swyftx",

    # Greenhouse companies
    "buildkite": "Buildkite",
    # Lever companies
    "immutable": "Immutable",
    # SmartRecruiters companies
    "carsales": "Carsales",
    
    # Add other mappings as needed
}

def get_or_create_company(proper_company_name: str):
    """Get an existing company or create a new one if it doesn't exist.
    
    Args:
        proper_company_name: The proper company name (e.g., 'Datacom', not 'datacom1')
        
    Returns:
        Company: The existing or newly created company object
        
    Raises:
        SQLAlchemyError: If there is a database error
        ValueError: If proper_company_name is empty or invalid
    """
    # Input validation
    if not proper_company_name or not isinstance(proper_company_name, str):
        logger.error(f"Invalid company name provided: {proper_company_name}")
        raise ValueError("Company name must be a non-empty string")

    try:
        with db.session.begin_nested():
            company = Company.query.filter_by(name=proper_company_name).first()
            if not company:
                logger.info(f"Creating new company: {proper_company_name}")
                company = Company(name=proper_company_name)
                db.session.add(company)
                db.session.flush()  # Flush to get the company ID
                logger.info(f"Successfully created company with ID: {company.company_id}")
            else:
                logger.info(f"Found existing company: {proper_company_name}")
            return company
            
    except SQLAlchemyError as e:
        logger.error(f"Database error while getting/creating company {proper_company_name}: {str(e)}")
        db.session.rollback()
        raise
    except Exception as e:
        logger.error(f"Unexpected error while getting/creating company {proper_company_name}: {str(e)}")
        db.session.rollback()
        raise

def get_existing_job_urls():
    """Get all existing jobpost_urls from the Jobs table"""
    try:
        existing_urls = db.session.query(Job.jobpost_url).all()
        return {url[0] for url in existing_urls if url[0]}  # Convert to set for O(1) lookup
    except SQLAlchemyError as e:
        logger.error(f"Error fetching existing job URLs: {e}")
        return set()

def run_scraper(input_data: Dict[str, Any]) -> List[Dict[str, Any]]:
    """Run the Actor and wait for it to finish, saving results to JSON file"""
    run = client.actor("8d7qNCKVcOhIALFgO").call(run_input=input_data)
    results = list(client.dataset(run["defaultDatasetId"]).iterate_items())
        
    # Get directory of current file
    current_dir = os.path.dirname(os.path.abspath(__file__))
    output_file = os.path.join(current_dir, 'scraper_results.json')
    
    # Write results to JSON file
    with open(output_file, 'w') as f:
        json.dump(results, f, indent=2)
        
    return results

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

        for company in items:
            allowed_departments = company_departments.get(company['name'], [])
            company_proper_name = get_proper_company_name(company['name'])
            
            logger.info(f"Processing jobs for {company_proper_name}")
            company_jobs = company['result']
            stats['total_scraped'] += len(company_jobs)

            for job in company_jobs:
                try:
                    # Check if job URL already exists
                    job_url = job.get('url')
                    if job_url in existing_urls:
                        stats['skipped_existing'] += 1
                        # logger.info(f"Skipping existing job: {job.get('title')} ({job_url})")
                        continue

                    processed_job = process_job(company['name'], company['source'], job)
                    if not processed_job:
                        stats['skipped_non_australia'] += 1
                        # logger.info(f"Skipping non-Australian job: {job.get('title')}")
                        continue

                    if allowed_departments and processed_job['department'] not in allowed_departments:
                        stats['skipped_department'] += 1
                        # logger.info(f"Skipping job with non-allowed department: {processed_job['department']}")
                        continue

                    # Get or create company
                    company_obj = get_or_create_company(processed_job['company'])
                    
                    # Prepare job details
                    job_details = {
                        'recruiter_id': 1,  # Admin recruiter ID
                        'company_id': company_obj.company_id,
                        'title': processed_job['title'],
                        'jobpost_url': job_url,
                        'city': processed_job['location'],
                        'country': 'Australia',
                        'description': processed_job['description'],
                        'department': processed_job.get('department', '')
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
                        raise Exception(f"Job with ID {new_job.job_id} not found after creation")
                    
                    stats['successfully_added'] += 1
                    logger.info(f"Successfully added and verified new job: {processed_job['title']} with ID {new_job.job_id}")

                except Exception as error:
                    stats['failed'] += 1
                    error_msg = f"Error processing job {job.get('title', 'Unknown')} for {company_proper_name}: {error}"
                    errors.append(error_msg)
                    logger.error(error_msg)
                    continue  # Continue with next job

        # Ensure final commit
        db.session.commit()

        # Log final statistics
        logger.info("\n=== Job Processing Statistics ===")
        logger.info(f"Total jobs scraped: {stats['total_scraped']}")
        logger.info(f"Jobs skipped (already exist): {stats['skipped_existing']}")
        logger.info(f"Jobs skipped (non-Australian): {stats['skipped_non_australia']}")
        logger.info(f"Jobs skipped (department): {stats['skipped_department']}")
        logger.info(f"Jobs successfully added: {stats['successfully_added']}")
        logger.info(f"Jobs failed to add: {stats['failed']}")
        logger.info(f"Total errors encountered: {len(errors)}")
        logger.info("=============================\n")

        return stats['successfully_added'], errors
        
    except Exception as e:
        db.session.rollback()
        raise

def process_job(company_name: str, source: str, job: Dict[str, Any]) -> Dict[str, Any]:
    if source == 'greenhouse':
        return process_greenhouse_job(company_name, job)
    elif source == 'workable':
        return process_workable_job(company_name, job)
    elif source == 'lever':
        return process_lever_job(company_name, job)
    elif source == 'smartrecruiters':
        return process_smartrecruiters_job(company_name, job)
    else:
        raise ValueError(f"Unknown source: {source}")

def is_job_in_australia(location: str, country_code: str = None) -> bool:
    australia_keywords = ['australia', 'au', 'aus', 'Melbourne', 'Sydney', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra', 'Wollongong', 'Sunshine Coast', 'Gold Coast', 'Newcastle', 'Canberra', 'Wollongong', 'Sunshine Coast']
    if country_code:
        return country_code.lower() in australia_keywords
    return any(keyword in location.lower() for keyword in australia_keywords)

def get_proper_company_name(identifier: str) -> str:
    """Convert company identifier to proper company name"""
    return company_name_mapping.get(identifier, identifier)  # Fallback to identifier if mapping not found

def process_greenhouse_job(company_name: str, job: Dict[str, Any]) -> Dict[str, Any]:
    location = job.get("location", "")
    if not is_job_in_australia(location):
        return None
    
    # Create the processed job data
    processed_job = {
        "company": get_proper_company_name(company_name),  # Use mapping here
        "title": job.get("title"),
        "location": location,
        "url": job.get("url"),
        "description": job.get("details", {}).get("description"),
        "department": job.get("department")
    }
    
    # Add logging for the processed job data
    # logger.info(f"Processed Greenhouse job: {processed_job}")
    
    return processed_job

def process_workable_job(company_name: str, job: Dict[str, Any]) -> Dict[str, Any]:
    location = job.get("location", "")
    country_code = job.get("details", {}).get("location", {}).get("countryCode")
    if not is_job_in_australia(location, country_code):
        return None
        
    processed_job = {
        "company": get_proper_company_name(company_name),  # Use mapping here
        "title": job.get("title"),
        "location": location,
        "url": job.get("url"),        
        "description": "\n\n".join([
            job.get("details", {}).get("description", ""),
            job.get("details", {}).get("requirements", ""),
            job.get("details", {}).get("benefits", ""),
        ]).strip(),
        "department": job.get("department")
    }
    
    # Add logging for the processed job data
    # logger.info(f"Processed Workable job: {processed_job}")
    
    return processed_job

def process_lever_job(company_name: str, job: Dict[str, Any]) -> Dict[str, Any]:
    location = job.get("location", "")
    if not is_job_in_australia(location):
        return None
    
    lists_content = []
    for item in job.get("details", {}).get("lists", []):
        lists_content.append(f"{item['text']}: {item['content']}")
    combined_lists = "\n".join(lists_content)
    description = f"{job.get('details', {}).get('descriptionPlain', '')}\n\n{combined_lists}"

    processed_job = {
        "company": get_proper_company_name(company_name),  # Use mapping here,
        "title": job.get("title"),
        "location": location,
        "url": job.get("url"),
        "description": description.strip(),
        "department": job.get("department")
    }
    
    # Add logging for the processed job data
    # logger.info(f"Processed Lever job: {processed_job}")
    
    return processed_job

def process_smartrecruiters_job(company_name: str, job: Dict[str, Any]) -> Dict[str, Any]:
    location = job.get("location", "")
    country_code = job.get("details", {}).get("location", {}).get("country")
    if not is_job_in_australia(location, country_code):
        return None

    # PROBLEM: Some of these values might be None, causing the join to fail
    # FIX: Filter out None values and provide default empty strings
    description_parts = [
        job.get("details", {}).get("jobAd", {}).get("sections", {}).get("companyDescription", {}).get("text", ""),
        job.get("details", {}).get("jobAd", {}).get("sections", {}).get("jobDescription", {}).get("text", ""),
        job.get("details", {}).get("jobAd", {}).get("sections", {}).get("qualifications", {}).get("text", ""),
        job.get("details", {}).get("jobAd", {}).get("sections", {}).get("additionalInformation", {}).get("text", "")
    ]

    # Filter out None values and empty strings
    description_parts = [part for part in description_parts if part]

    processed_job = {
        "company": get_proper_company_name(company_name),
        "title": job.get("title"),
        "location": location,
        "url": job.get("url"),
        "description": "\n\n".join(description_parts).strip(),
        "department": job.get("department")
    }
    
    # Add logging for the processed job data
    logger.info(f"Processed SmartRecruiters job: {processed_job}")
    
    return processed_job

# Usage
if __name__ == "__main__":
    with app.app_context():  # This is the key addition
        input_data = {
        "customquery": {
            "buildkite": "greenhouse",
            "compass-education": "workable",
            "immutable": "lever",
            "octoenergy": "lever",
            "xero": "lever",
            "recordpoint": "lever",
            "myob": "lever",
            "blinq": "lever",
            # "octopus": "lever",
            # "Zeller": "lever",
            # "swyftx": "lever",
            # "carsales": "smartrecruiters"
    },
    "delay": 10,
    "details": "Yes",
    "greenhouse": True,
    "lever": True,
    "personio": False,
    "proxy": {
        "useApifyProxy": True,
        "apifyProxyGroups": [
            "RESIDENTIAL"
        ]
    },
    "recruitee": False,
    "smartrecruiters": True,
    "workable": True,
    "workday": False
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

@celery.task(
    name='scrapers.ats_scraper.run_scheduled_scraper',
    rate_limit='1/h',           # Max 1 run per hour
    soft_time_limit=1500,       # 25 minutes soft timeout
    time_limit=1800,            # 30 minutes hard timeout
    max_retries=1,              # Only retry once
    retry_backoff=300,          # 5 minutes between retries
)
def run_scheduled_scraper():
    with app.app_context():
        input_data = {
            "customquery": {
                "buildkite": "greenhouse",
                "compass-education": "workable",
                "immutable": "lever",
                "octoenergy": "lever",
                "xero": "lever",
                "recordpoint": "lever",
                "myob": "lever",
                "blinq": "lever",
            },
            "delay": 10,
            "details": "Yes",
            "greenhouse": True,
            "lever": True,
            "personio": False,
            "proxy": {
                "useApifyProxy": True,
                "apifyProxyGroups": ["RESIDENTIAL"]
            },
            "recruitee": False,
            "smartrecruiters": True,
            "workable": True,
            "workday": False
        }

        try:
            logger.info("Starting job scraping process...")
            results = run_scraper(input_data)
            successful_adds, errors = process_results(results)
            
            # Get the stats from process_results
            stats = {
                'total_scraped': len(results),
                'successfully_added': successful_adds,
                'skipped_existing': len(results) - successful_adds - len(errors),
                'failed': len(errors)
            }
            
            # Send email report
            send_scraper_report('ATS', stats, errors)
            
            return {'successful_adds': successful_adds, 'errors': errors}
        except Exception as e:
            logger.error(f"Fatal error during scraping: {str(e)}", exc_info=True)
            # Send error notification
            send_scraper_report('ATS', 
                              {'failed': 1, 'total_scraped': 0, 'successfully_added': 0}, 
                              [f"Fatal error: {str(e)}"])
            raise

