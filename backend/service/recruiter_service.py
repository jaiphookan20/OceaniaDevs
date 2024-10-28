from extensions import db
from models import Job, Recruiter, Company, TechnologyAlias, Technology, JobTechnology, Application, Bookmark, salary_type_enum, contract_duration_enum, daily_range_enum, hourly_range_enum
from service.jobs_service import JobsService    
from flask import session, jsonify, current_app, request
from utils.categorize import categorize_words
import requests
import json
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
from utils.openai import OpenAI
from utils.time import get_relative_time
import concurrent.futures
from concurrent.futures import TimeoutError
from sqlalchemy.exc import SQLAlchemyError
import time
from extensions import cache
import config
from datetime import datetime, timedelta
import random
from urllib.parse import urlparse
from flask_mail import Message
from extensions import mail
import logging

load_dotenv()

class RecruiterService:
    def __init__(self):
        self.api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.openai_client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))
        # self.headers = {
        #     "Authorization": f"Bearer {os.getenv('DEEPINFRA_API_KEY')}",
        #     "Content-Type": "application/json"
        # }
        current_app.logger.info("RecruiterService initialized.")

    def get_recruiter_by_id(self, recruiter_id):
        try:
            recruiter = Recruiter.query.get(recruiter_id)
            if not recruiter:
                current_app.logger.warning(f"Recruiter with id {recruiter_id} not found")
            return recruiter
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_recruiter_by_id: {str(e)}")
            return None

    def get_all_jobs_by_recruiter(self, recruiter_id):
        try:
            jobs = Job.query.filter_by(recruiter_id=recruiter_id).order_by(Job.created_at.desc()).all()
            current_app.logger.info(f"Retrieved {len(jobs)} jobs for recruiter {recruiter_id}")
            return jobs
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_all_jobs_by_recruiter: {str(e)}")
            return []

    def get_company_by_recruiter_id(self):
        try:
            if 'user' not in session or session['user']['type'] != 'recruiter':
                current_app.logger.warning("Unauthorized access attempt in get_company_by_recruiter_id")
                return None
            recruiter_id = session['user']['recruiter_id']
            recruiter = Recruiter.query.get(recruiter_id)
            if not recruiter:
                current_app.logger.warning(f"Recruiter with id {recruiter_id} not found")
                return None
            company = Company.query.get(recruiter.company_id)
            if not company:
                current_app.logger.warning(f"Company not found for recruiter {recruiter_id}")
            return company
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_company_by_recruiter_id: {str(e)}")
            return None

    def update_recruiter_info(self, recruiter_id, data):
        try:
            recruiter = self.get_recruiter_by_id(recruiter_id)
            if not recruiter:
                current_app.logger.warning(f"Recruiter with id {recruiter_id} not found for update")
                return False
            
            recruiter.first_name = data.get('firstName', recruiter.first_name)
            recruiter.last_name = data.get('lastName', recruiter.last_name)
            recruiter.position = data.get('position', recruiter.position)
            
            db.session.commit()
            current_app.logger.info(f"Successfully updated info for recruiter {recruiter_id}")
            return True
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in update_recruiter_info: {str(e)}")
            db.session.rollback()
            return False

    def update_recruiter_company(self, recruiter_id, data, logo):
        try:
            recruiter = self.get_recruiter_by_id(recruiter_id)
            if recruiter and recruiter.company_id:
                company = Company.query.get(recruiter.company_id)
                if company:
                    company.size = data.get('employerSize', company.size)
                    company.website_url = data.get('employerWebsite', company.website_url)
                    company.description = data.get('employerDescription', company.description)[:200]
                    company.type = data.get('type', company.type)
                    company.city = data.get('city', company.city)
                    company.state = data.get('state', company.state)
                    company.industry = data.get('industry', company.industry)
                    
                    if logo:
                        filename = secure_filename(logo.filename)
                        logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], filename)
                        logo.save(logo_path)
                        company.logo_url = f"/uploads/upload_company_logo/{filename}"
                    
                    try:
                        db.session.commit()
                        current_app.logger.info(f"Successfully updated company info for recruiter {recruiter_id}")
                        return True
                    except SQLAlchemyError as e:
                        current_app.logger.error(f"Database error in update_recruiter_company: {str(e)}")
                        db.session.rollback()
                        return False
            current_app.logger.warning(f"Company not found for recruiter {recruiter_id}")
            return False
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in update_recruiter_company: {str(e)}")
            db.session.rollback()
            return False

    def create_company(self, recruiter_id, data, logo_file):
        try:
            logo_path = None
            if logo_file:
                logo_filename = secure_filename(logo_file.filename)
                logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename)
                logo_file.save(logo_path)

            new_company = Company(
                name=data.get('employerName'),
                website_url=data.get('employerWebsite'),
                size=data.get('employerSize'),
                description=data.get('employerDescription'),
                # location=data.get('location'),
                logo_url=logo_path,
                type=data.get('type'),
                industry=data.get('industry'),
                city=data.get('city'),
                state=data.get('state')
            )

            db.session.add(new_company)
            db.session.commit()

            recruiter = self.get_recruiter_by_id(recruiter_id)
            recruiter.company_id = new_company.company_id
            db.session.commit()

            current_app.logger.info(f"Successfully created company for recruiter {recruiter_id}")
            return True
        except Exception as e:
            current_app.logger.error(f"Error in create_company: {str(e)}")
            db.session.rollback()
            return False

    def process_job_description_openai(self, title, description):
        # First API call: Extract basic job information
        basic_info = self._extract_basic_job_info(title, description)
        
        # Second API call: Extract detailed job requirements and responsibilities
        detailed_info = self._extract_detailed_job_info(title, description, basic_info)

        # Combine the results
        processed_data = {**basic_info, **detailed_info}

        return processed_data

    def _extract_basic_job_info(self, title, description):
        try:
            messages = [
                {
                    "role": "system",
                    "content": "You are an AI assistant specializing in job market analysis. Extract basic job information from the given title and description."
                },
                {
                    "role": "user",
                    "content": f"""Analyze the following job description and title. Provide a response in JSON format with these keys: 'specialization', 'technologies', 'industry', 'work_location', 'min_experience_years', 'experience_level', 'city', 'state', 'job_arrangement', 'citizens_or_pr_only', 'security_clearance_required'.

                    Title: {title}
                    Job Description: {description}

                    Instructions:
                    1. 'specialization': Classify the job into ONLY ONE of these categories: Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity'.
                    2. 'technologies': List specific software technologies mentioned (e.g., Java, TypeScript, React, AWS). Exclude general terms like 'LLM services', 'Containers', 'CI/CD' or 'REST APIs'.
                    3. 'industry': Identify the end market or industry of the client that the role serves. If client is federal government, industry = 'government'. Use one of the following: ['Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics'].
                    4. 'work_location': Specify the work location as one of: 'Remote', 'Hybrid', 'Office'. Default option: 'Office'.
                    5. 'min_experience_years': Extract the highest number of years of experience mentioned for any skill. Provide only numeric values or 0 if not specified.
                    6. 'experience_level': Classify as you deem fit into one of: 'Junior', 'Mid-Level', 'Senior', or 'Executive' based on the experience requirements defined in the role and/or title.
                    7. 'city': Extract the city where the job is located. Strictly only do so if mentioned, otherwise empty.
                    8. 'state': Extract the state where the job is located. Use one of the following: ['VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA']. Strictly only do so if mentioned, otherwise empty.
                    9. 'citizens_or_pr_only': Set to true if the job description explicitly states that only Australian citizens or permanent residents can apply. Otherwise, set to false.
                    10. 'security_clearance_required': Set to true if the job description mentions any level of security clearance requirement (Baseline, Negative Vetting 1, Negative Vetting 2, or Positive Vetting). Otherwise, set to false.

                    Provide only the JSON object as output, with no additional text.
                    - For 'technologies', use an array of strings, each representing a single technology.
                    
                    """
                }
            ]
        
            # Make API call and process response
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                response_format={"type": "json_object"}
            )
            data = json.loads(response.choices[0].message.content)

            # Validate and fallback for each field
            validated_data = {
                'work_location': (data.get('work_location') 
                                if data.get('work_location') in ['Remote', 'Hybrid', 'Office'] 
                                else 'Office'),
                'job_arrangement': (data.get('job_arrangement') 
                                if data.get('job_arrangement') in ['Permanent', 'Contract/Temp', 'Internship', 'Part-Time'] 
                                else 'Permanent'),
                'experience_level': (data.get('experience_level') 
                                if data.get('experience_level') in ['Junior', 'Mid-Level', 'Senior', 'Executive'] 
                                else 'Mid-Level')
            }
            
            return validated_data
        
        except Exception as e:
            current_app.logger.error(f"Error in _extract_basic_job_info: {str(e)}")
            # Return safe default values that match enum constraints
            return {
                'work_location': 'Office',
                'job_arrangement': 'Permanent',
                'experience_level': 'Mid-Level'
            }

    def _extract_detailed_job_info(self, title, description, basic_info):
        try:
            messages = [
                {
                "role": "system",
                "content": "You are an AI assistant specializing in detailed job analysis. Extract specific job requirements and responsibilities from the given title and description."
            },
            {
                "role": "user",
                "content": f"""Analyze the following job description and title. Provide a response in JSON format with these keys: 'overview', 'responsibilities', 'requirements', 'technologies', 'salary_type', 'salary_range', 'hourly_range', 'daily_range', 'job_arrangement','contract_duration'.

                Title: {title}
                Job Description: {description}
                Basic Info: {json.dumps(basic_info)}

                Instructions:
                1. 'overview': Summarize the role and company, including all key and salient information relevant to potential candidates. Add any information related to benefits or perks here. Add information verbatim if needed but all of the information is needed. Provide a String response.
                2. 'responsibilities': List main job duties and expectations. Provide detailed information. 
                3. 'requirements': Enumerate essential qualifications and skills needed. Provide detailed information. 
                4. 'salary_type': If only available the type of salary is availabe and mentioned, specify the type of salary or payment arrangement. Choose ONLY one of the following: ['annual', 'hourly', 'daily']. If Unavailable, choose 'annual'.
                5. 'salary_range': If only the salary is available AND salary_type="annual", extract the salary information and classify it in the bucket it fits in: 'Not Listed', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+'. If Unavailable, choose 'Not Listed'.
                6. 'hourly_range': If only the hourly pay information is available AND salary_type="hourly", extract the hourly-rate information and classify it in the bucket it fits in: 'Not Listed', '0-20', '20-40', '40-60', '60-80', '80-100', '100-120', '120-140', '140-160', '160+'. If Unavailable, choose 'Not Listed'.
                7. 'daily_range': If only the daily pay information is available AND salary_type="daily", extract the daily-rate information and classify it in the bucket it fits in: 'Not Listed', '0-200', '200-400', '400-600', '600-800', '800-1000', '1000-1200', '1200-1400', '1400-1600', '1600+'. If Unavailable, choose 'Not Listed'.
                8. 'job_arrangement': Specify the job arrangement as ONLY one of: 'Permanent', 'Contract/Temp', 'Part-Time' or 'Internship'. Strictly do not include any other value. Classify as Contract/Temp if the job is a contract or temporary job.
                9. 'contract_duration': If only the 'job_arrangement' is 'Contract/Temp', and if the duration of the contract is provided and available, classify it as belonging to one of the following buckets: 'Not Listed', '0-3 months', '4-6 months', '7-9 months', '10-12 months' or '12+ months'. If unavailable, choose 'Not Listed'.

                Ensure the following:
                - Provide only the JSON object as output, with no additional text.
                - For 'responsibilities' and 'requirements', use arrays of strings.
                - If information for a key is not available, use an empty string or array as appropriate.
                """
            }
        ]
        
            # Make API call and process response
            response = self.openai_client.chat.completions.create(
                model="gpt-4o",
                messages=messages,
                response_format={"type": "json_object"}
            )
            
            data = json.loads(response.choices[0].message.content)
        
            # Validate and fallback for each field
            validated_data = {
                'contract_duration': (data.get('contract_duration') 
                                    if data.get('contract_duration') in ['Not Listed', '0-3 months', '4-6 months', '7-9 months', '10-12 months', '12+ months'] 
                                    else 'Not Listed'),
                'salary_type': (data.get('salary_type') 
                            if data.get('salary_type') in ['annual', 'hourly', 'daily'] 
                            else 'annual'),
                'min_experience_years': int(data.get('min_experience_years', 0)) if str(data.get('min_experience_years', '')).isdigit() else 0,
                'daily_range': (data.get('daily_range') 
                            if data.get('daily_range') in ['Not Listed', '0-200', '200-400', '400-600', '600-800', '800-1000', '1000-1200', '1200-1400', '1400-1600', '1600+'] 
                            else 'Not Listed'),
                'hourly_range': (data.get('hourly_range') 
                            if data.get('hourly_range') in ['Not Listed', '0-20', '20-40', '40-60', '60-80', '80-100', '100-120', '120-140', '140-160', '160+'] 
                            else 'Not Listed')
            }
            
            return validated_data
        
        except Exception as e:
            current_app.logger.error(f"Error in _extract_detailed_job_info: {str(e)}")
            # Return safe default values that match enum constraints
            return {
                'contract_duration': 'Not Listed',
                'salary_type': 'annual',
                'min_experience_years': 0,
                'daily_range': 'Not Listed',
                'hourly_range': 'Not Listed'
            }

    def _verify_and_correct_job_info(self, title, description, processed_data):
        # Define the acceptable values for each field
        field_constraints = {
            "specialization": ["Frontend", "Backend", "Full-Stack", "Mobile", "Data & ML", "QA & Testing", "Cloud & Infra", "DevOps", "Project Management", "IT Consulting", "Cybersecurity"],
            "experience_level": ["Junior", "Mid-Level", "Senior", "Executive"],
            "work_location": ["Remote", "Hybrid", "Office"],
            "job_arrangement": ["Permanent", "Contract/Temp", "Internship", "Part-Time"],
            "salary_type": ["annual", "hourly", "daily"],
            "salary_range": ["Not Listed", "20000 - 40000", "40000 - 60000", "60000 - 80000", "80000 - 100000", "100000 - 120000", "120000 - 140000", "140000 - 160000", "160000 - 180000", "180000 - 200000", "200000 - 220000", "220000 - 240000", "240000 - 260000", "260000+"],
            "hourly_range": ["Not Listed", "0-20", "20-40", "40-60", "60-80", "80-100", "100-120", "120-140", "140-160", "160+"],
            "daily_range": ["Not Listed", "0-200", "200-400", "400-600", "600-800", "800-1000", "1000-1200", "1200-1400", "1400-1600", "1600+"],
            "contract_duration": ["Not Listed", "0-3 months", "4-6 months", "7-9 months", "10-12 months", "12+ months"],
            "industry": ["Government", "Banking & Financial Services", "Fashion", "Mining", "Healthcare", "IT - Software Development", "IT - Data Analytics", "IT - Cybersecurity", "IT - Cloud Computing", "IT - Artificial Intelligence", "Agriculture", "Automotive", "Construction", "Education", "Energy & Utilities", "Entertainment", "Hospitality & Tourism", "Legal", "Manufacturing", "Marketing & Advertising", "Media & Communications", "Non-Profit & NGO", "Pharmaceuticals", "Real Estate", "Retail & Consumer Goods", "Telecommunications", "Transportation & Logistics"],
        }

        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant specialized in verifying and correcting job information. Your task is to ensure the extracted job details are accurate, consistent with the original job description, and conform to the specified field constraints."
            },
            {
                "role": "user",
                "content": f"""Review the following job title, description, and extracted information. Verify if the extracted information is correct, consistent with the job description, and conforms to the specified field constraints. If any information is incorrect, missing, or doesn't conform to the constraints, provide the correct information. Respond in JSON format with the corrected information.

                Job Title: {title}
                Job Description: {description}
                
                Extracted Information:
                {json.dumps(processed_data, indent=2)}

                Field Constraints:
                {json.dumps(field_constraints, indent=2)}

                Instructions:
                1. Review each field in the extracted information.
                2. If a field is correct and conforms to the constraints, keep it as is.
                3. If a field is incorrect, missing, or doesn't conform to the constraints, provide the correct value based on the job description and the given constraints. ONLY provide the corrected value from the list of acceptable values in 'field_constraints', no additional text.
                4. If a field is not mentioned in the job description and cannot be inferred, leave it as is or set it to an appropriate default value (e.g., "Not Listed" for salary ranges).
                5. Ensure all fields from the original extracted information are included in your response, even if unchanged.
                6. Pay special attention to 'specialization', 'technologies', 'experience_level', and 'salary_range' to ensure they are accurate and conform to the constraints.

                Provide only the JSON object as output, with no additional text.
                """
            }
        ]

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini",
                messages=messages,
                response_format={"type": "json_object"}
            )
            verified_data = json.loads(response.choices[0].message.content)
            current_app.logger.info("Successfully verified and corrected job information")
            return verified_data

        except Exception as e:
            current_app.logger.error(f"OpenAI API request failed in verification step: {str(e)}")
            return processed_data  # Return the original processed data if verification fails
    
    def add_job_programmatically_admin(self, job_data):
        """Add a job programmatically with admin privileges."""
        try:
            title = job_data.get('title')
            description = job_data.get('description')
            current_app.logger.info(f"Processing job: {title}")

            # Process with OpenAI
            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.process_job_description_openai, title, description)
                try:
                    processed_data = future.result(timeout=180)
                except TimeoutError:
                    current_app.logger.error(f"OpenAI API call timed out for job: {title}")
                    return None, "OpenAI API call timed out after 3 minutes"

            if not processed_data:
                error_msg = f"Failed to process job description for: {title}"
                current_app.logger.error(error_msg)
                return None, error_msg

            try:
                # Create new job instance with proper enum values
                new_job = Job(
                    recruiter_id=job_data.get('recruiter_id', 1),  # Default to admin recruiter
                    company_id=job_data.get('company_id'),
                    title=job_data.get('title'),
                    description=job_data.get('description'),
                    overview=processed_data.get('overview', ''),
                    responsibilities=processed_data.get('responsibilities', []),
                    requirements=processed_data.get('requirements', []),
                    city=job_data.get('city', ''),
                    state=job_data.get('state', ''),
                    country=job_data.get('country', 'Australia'),
                    jobpost_url=job_data.get('jobpost_url', ''),
                    work_location=processed_data.get('work_location', 'Not Specified'),
                    work_rights=processed_data.get('work_rights'),
                    job_arrangement=processed_data.get('job_arrangement', 'Permanent'),
                    specialization=processed_data.get('specialization', 'Not Specified'),
                    job_type=processed_data.get('job_type', 'normal'),
                    industry=processed_data.get('industry', 'Not Specified'),
                    min_experience_years=processed_data.get('min_experience_years', 0),
                    experience_level=processed_data.get('experience_level', 'Not Specified'),
                    tech_stack=None,  # Will be processed separately
                    salary_range=processed_data.get('salary_range', 'Not Specified'),
                    salary_type=processed_data.get('salary_type', 'not_specified'),  # Using enum value
                    contract_duration=processed_data.get('contract_duration', 'not_specified'),  # Using enum value
                    daily_range=processed_data.get('daily_range', 'not_specified'),  # Using enum value
                    hourly_range=processed_data.get('hourly_range', 'not_specified'),  # Using enum value
                    citizens_or_pr_only=processed_data.get('citizens_or_pr_only', False),
                    security_clearance_required=processed_data.get('security_clearance_required', False)
                )

                # Add to session and flush to get the job_id
                db.session.add(new_job)
                db.session.flush()

                # Process technologies if available
                tech_stack = processed_data.get('technologies', [])
                if tech_stack:
                    current_app.logger.info(f"Processing technologies for job '{title}': {tech_stack}")
                    added_techs = self._process_technologies(new_job, tech_stack)
                    current_app.logger.info(f"Added technologies for job '{title}': {added_techs}")

                # Commit the transaction
                db.session.commit()
                current_app.logger.info(f"Successfully added job: {title}")
                return new_job, None

            except SQLAlchemyError as db_error:
                db.session.rollback()
                error_msg = f"Database error while adding job: {str(db_error)}"
                current_app.logger.error(error_msg)
                return None, error_msg

        except Exception as e:
            if isinstance(e, SQLAlchemyError):
                db.session.rollback()
            error_msg = f"Error adding job '{job_data.get('title', 'Unknown')}': {str(e)}"
            current_app.logger.error(error_msg, exc_info=True)
            return None, error_msg

    def _process_technologies(self, job, tech_stack):
        normalized_technologies = set(self.normalize_technology_name(tech) for tech in tech_stack if tech)
        for tech_name in normalized_technologies:
            technology = Technology.query.filter_by(name=tech_name).first()
            if technology:
                job_tech = JobTechnology(job=job, technology=technology)
                db.session.add(job_tech)
        current_app.logger.info(f"Added technologies for job '{job.title}': {normalized_technologies}")

    def normalize_technology_name(self, tech_name):
        """Normalize technology names using the technology_aliases table."""
        # Print/log the technology name before normalization
        current_app.logger.info(f"Normalizing technology name: {tech_name}")
        
        alias_entry = TechnologyAlias.query.filter(db.func.lower(TechnologyAlias.alias) == tech_name.lower()).first()
        if alias_entry:
            normalized_name = alias_entry.technology.name
            # Print/log the normalized technology name
            current_app.logger.info(f"Found normalized name: {normalized_name} for alias: {tech_name}")
            return normalized_name
        else:
            # Log if no normalization is found
            current_app.logger.info(f"No normalized name found for alias: {tech_name}")
            return None    

    # NEED TO UPDATE ON FRONTEND FOR SALARY_TYPE, CONTRACT_DURATION, DAILY_RANGE, and HOURLY_RANGE
    def update_job(self, job_id, data):
        try:
            job = Job.query.get(job_id)
            if not job:
                current_app.logger.warning(f"Job with id {job_id} not found for update")
                return None
            
            for key, value in data.items():
                if key == 'salary_type':
                    setattr(job, key, salary_type_enum(value))
                elif key == 'contract_duration':
                    setattr(job, key, contract_duration_enum(value))
                elif key == 'daily_range':
                    setattr(job, key, daily_range_enum(value))
                elif key == 'hourly_range':
                    setattr(job, key, hourly_range_enum(value))
                else:
                    setattr(job, key, value)
            
            db.session.commit()

            # Invalidate relevant caches
            self.invalidate_job_caches(job)

            # Invalidate the specific job post cache
            cache.delete_memoized(JobsService.get_job_post_data, job_id)

            current_app.logger.info(f"Successfully updated job {job_id}")
            return job
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in update_job: {str(e)}")
            db.session.rollback()
            return None
        
    def remove_job(self, job_id, recruiter_id):
        try:
            job = Job.query.filter_by(job_id=job_id, recruiter_id=recruiter_id).first()
            if not job:
                current_app.logger.warning(f"Job with id {job_id} not found for removal")
                return {'success': False, 'error': 'not_found'}

            # Delete related records
            JobTechnology.query.filter_by(job_id=job_id).delete()
            Application.query.filter_by(jobid=job_id).delete()
            Bookmark.query.filter_by(jobid=job_id).delete()

            # Delete the job
            db.session.delete(job)
            db.session.commit()

            # Invalidate relevant caches
            self.invalidate_job_caches(job)

            current_app.logger.info(f"Successfully removed job {job_id}")
            return {'success': True}

        except SQLAlchemyError as e:
            db.session.rollback()
            current_app.logger.error(f"Database error in remove_job: {str(e)}")
            return {'success': False, 'error': 'database_error'}
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Unexpected error in remove_job: {str(e)}")
            return {'success': False, 'error': 'unexpected_error'}
        
    # Still not working correctly
    def _get_email_domain(self, company_id):
        # Retrieve the company by its ID
        company = Company.query.get(company_id)
        
        # Check if the company exists and has a website URL
        if company and company.website_url:
            # Strip whitespace and convert to lowercase
            url = company.website_url.strip().lower()
            
            # Ensure the URL starts with 'http://' or 'https://'
            if not url.startswith(('http://', 'https://')):
                url = 'https://' + url
            
            # Parse the URL to extract components
            parsed_url = urlparse(url)
            
            # Get the domain from netloc or path
            domain = parsed_url.netloc or parsed_url.path
            
            # Handle cases where there may be a port number in the domain
            if ':' in domain:
                domain = domain.split(':')[0]
            
            # Split the domain into parts
            parts = domain.split('.')
            
            # Determine the appropriate domain format based on TLDs
            if len(parts) > 2:
                # If the last part is a common TLD, include the last three parts
                if parts[-1] in ['com', 'org', 'net', 'edu', 'gov', 'mil']:
                    domain = '.'.join(parts[-3:])
                else:
                    # Otherwise, include the last two parts
                    domain = '.'.join(parts[-2:])
            
            # Remove 'www.' if it exists at the start of the domain
            return domain.replace('www.', '')
        
        return None
    
    @cache.cached(timeout=3600)
    def get_all_companies(self):
        try:
            companies = Company.query.all()


            company_data = [{
                "company_id": company.company_id,
                "name": company.name,
                "description": company.description,
                "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                "size": company.size,
                "address": company.address,
                "job_count": self.get_job_count_for_company(company.company_id),
                "website_url": company.website_url,
                "domain": self._get_email_domain(company.company_id),
            } for company in companies]
            current_app.logger.info(f"Retrieved {len(companies)} companies")
            return company_data
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_all_companies: {str(e)}")
            return []

    def invalidate_job_caches(self, job):
        try:
            cache.delete_memoized(JobsService.get_home_page_jobs)
            cache.delete_memoized(JobsService.filtered_search_jobs)
            cache.delete_memoized(JobsService.instant_search_jobs)
            cache.delete_memoized(JobsService.get_home_page_jobs, job.specialization)
            current_app.logger.info(f"Cache invalidated for job {job.job_id}")
        except Exception as e:
            current_app.logger.error(f"Error invalidating cache: {str(e)}")

    def get_companies_with_pagination(self, page, page_size, search, industries, types):
        try:
            query = Company.query
            
            current_app.logger.info(f"Search query: {search}")
            current_app.logger.info(f"Industries filter: {industries}")
            current_app.logger.info(f"Types filter: {types}")
            
            if search:
                query = query.filter(Company.name.ilike(f'%{search}%'))
            
            if industries and 'all' not in industries:
                query = query.filter(Company.industry.in_(industries))
            
            if types and 'all' not in types:
                query = query.filter(Company.type.in_(types))
            
            current_app.logger.info(f"Filtered query: {query}")
            
            total_companies = query.count()
            current_app.logger.info(f"Total companies after filter: {total_companies}")
            
            companies = query.order_by(Company.name).paginate(page=page, per_page=page_size, error_out=False).items
            
            company_data = [{
                "company_id": company.company_id,
                "name": company.name,
                "description": company.description,
                "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                "address": company.address,
                "city": company.city,
                "state": company.state,
                "industry": company.industry,
                "type": company.type,
                "job_count": self.get_job_count_for_company(company.company_id)
            } for company in companies]
            
            current_app.logger.info(f"Retrieved {len(companies)} companies with pagination")
            return company_data, total_companies
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_companies_with_pagination: {str(e)}")
            return [], 0

    def get_job_count_for_company(self, company_id):
        try:
            job_count = Job.query.filter_by(company_id=company_id).count()
            current_app.logger.info(f"Retrieved job count for company {company_id}: {job_count}")
            return job_count
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_job_count_for_company: {str(e)}")
            return 0
    
    @cache.memoize(timeout=3600)
    def get_company_details(self, company_id):
        try:
            company = Company.query.get(company_id)
            if not company:
                current_app.logger.warning(f"Company with id {company_id} not found")
                return None
            
            # Get non-expired jobs and order by creation date
            thirty_days_ago = datetime.now() - timedelta(days=30)
            jobs = Job.query.filter_by(company_id=company_id).filter(Job.created_at >= thirty_days_ago).order_by(Job.created_at.desc()).all()
            job_count = len(jobs)
            
           # Collect all unique technologies for all jobs of this company
            unique_tech_stack = set()
            for job in jobs:
                # Fetch technologies for each job using JobTechnology
                technologies = db.session.query(Technology.name).join(JobTechnology, Technology.id == JobTechnology.technology_id).filter(JobTechnology.job_id == job.job_id).all()
                unique_tech_stack.update(tech[0] for tech in technologies)
            
            # Convert set to sorted list
            unique_tech_stack = sorted(unique_tech_stack)
            
            company_data = {
                "company_id": company.company_id,
                "name": company.name,
                "description": company.description,
                "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                "size": company.size,
                "website_url": company.website_url,
                "total_jobs": job_count,
                "city": company.city,
                "state": company.state,
                "industry": company.industry,
                "total_tech_stack": unique_tech_stack,
                "jobs": [{
                    "job_id": job.job_id,
                    "title": job.title,
                    "description": job.description,
                    "specialization": job.specialization,
                    "job_type": job.job_type,
                    "salary_range": job.salary_range,
                    "work_location": job.work_location,
                    "experience_level": job.experience_level,
                    "created_at": job.created_at,
                } for job in jobs],
            }
            
            current_app.logger.info(f"Retrieved company details for company {company_id}")
            return company_data
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_company_details: {str(e)}")
            return None

    def get_recommended_jobs(self, job_id):
        try:
            current_job = Job.query.get(job_id)
            if not current_job:
                current_app.logger.warning(f"Job with id {job_id} not found")
                return []
            
            recommended_jobs = Job.query.filter(
                Job.specialization == current_job.specialization,
                Job.job_id != job_id
            ).order_by(Job.created_at.desc()).limit(6).all()
            
            result = []
            for job in recommended_jobs:
                company = Company.query.get(job.company_id)
                result.append({
                    "job_id": job.job_id,
                    "title": job.title,
                    "company_id": company.company_id,
                    "company_name": company.name,
                    "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                    "location": f"{job.city}",
                    "salary_range": job.salary_range,
                    "experience_level": job.experience_level,
                    'specialization': job.specialization,
                    'min_experience_years': job.min_experience_years,
                    "created_at": get_relative_time(job.created_at.strftime("%Y-%m-%d"))
                })
            
            current_app.logger.info(f"Retrieved recommended jobs for job {job_id}")
            return result
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in get_recommended_jobs: {str(e)}")
            return []

    def process_resume(self, resume_text):
        messages = [
            {
                "role": "system",
                "content": "You are an AI assistant specialized in analyzing resumes and extracting specific information."
            },
            {
                "role": "user",
                "content": f"""Analyze the following resume and extract the requested information if available. Provide a response in JSON format with these keys: 'name', 'email', 'city', 'state', 'education', 'gpa', 'grade', 'work_experience', 'technologies', 'projects'.

                Instructions for each key:
                1. 'name': Full name of the applicant.
                2. 'email': Email address of the applicant.
                3. 'city': City of residence.
                4. 'state': State of residence.
                5. 'education': An array of objects, each with 'university', 'degree', and 'graduation_year'.
                6. 'gpa': GPA if mentioned.
                7. 'grade': Overall grade if mentioned.
                8. 'work_experience': An array of objects, each with 'company', 'position', 'duration', and 'responsibilities'.
                9. 'technologies': An array of technologies, programming languages, and tools mentioned.
                10. 'projects': An array of objects, each with 'name' and 'description'.

                Important:
                - If any information is not available in the resume, omit that key from the JSON response.
                - For work experience, structure the information properly and include all relevant details.
                - Ensure all extracted information is accurate and properly formatted.

                Resume Text: {resume_text}
                """
            }
        ]

        try:
            response = self.openai_client.chat.completions.create(
                model="gpt-4o-mini", 
                messages=messages,
                response_format={"type": "json_object"}
            )

            content = response.choices[0].message.content
            processed_data = json.loads(content)
            current_app.logger.info("Successfully processed resume")
            return processed_data

        except Exception as e:
            current_app.logger.error(f"OpenAI API request failed: {str(e)}")
            return None

    def process_jobs_from_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file_path = os.path.join(current_dir, 'jdp_jobs.json')
        output_file_path = os.path.join(current_dir, 'processing_results.json')

        try:
            with open(input_file_path, 'r') as file:
                jobs_data = json.load(file)
        except FileNotFoundError:
            yield json.dumps({"error": f"Input file {input_file_path} not found"})
            return
        except json.JSONDecodeError:
            yield json.dumps({"error": f"Invalid JSON in {input_file_path}"})
            return

        excluded_categories = ["PR & Communications", "Digital Marketing", "SEO/SEM"]
        filtered_jobs = [job for job in jobs_data if job['category'] not in excluded_categories]
        
        recruiter_id = 15
        company_id = 10
        results = []
        
        for job in filtered_jobs:
            try:
                job_data = {
                    'recruiter_id': recruiter_id,
                    'company_id': company_id,
                    'title': job['title'],
                    'description': job['description'],
                    'jobpost_url': job['url'],
                    'job_arrangement': job['jobType'],
                    'city': job['jobHighlights']['location'],
                    'country': 'Australia',  
                }
                
                start_time = time.time()
                new_job, error = self.add_job_programmatically(job_data)
                processing_time = time.time() - start_time

                if new_job:
                    processed_data = {
                        'job_id': new_job.job_id,
                        'title': new_job.title,
                        'description': new_job.description,
                        'jobpost_url': new_job.jobpost_url,
                        'job_arrangement': new_job.job_arrangement,
                        'city': new_job.city,
                        'country': new_job.country,
                        'specialization': new_job.specialization,
                        'industry': new_job.industry,
                        'salary_range': new_job.salary_range,
                        'work_location': new_job.work_location,
                        'experience_level': new_job.experience_level,
                        'tech_stack': new_job.tech_stack,
                    }
                else:
                    processed_data = None

                result = {
                    'title': job['title'],
                    'success': error is None,
                    'error': str(error) if error else None,
                    'processed_data': processed_data,
                    'processing_time': processing_time
                }

                results.append(result)
                yield json.dumps(result) + "\n"
            
            except Exception as e:
                error_result = {
                    'title': job.get('title', 'Unknown'),
                    'success': False,
                    'error': f"Unexpected error: {str(e)}",
                    'processed_data': None
                }
                results.append(error_result)
                yield json.dumps(error_result) + "\n"
            
            # Add a small delay between processing jobs to prevent overwhelming the API
            time.sleep(1)
        
        try:
            with open(output_file_path, 'w') as file:
                json.dump(results, file, indent=2)
            yield json.dumps({"message": f"Processing complete. Results saved to {output_file_path}"})
        except IOError as e:
            yield json.dumps({"error": f"Error saving results: {str(e)}"})

    def update_existing_jobs_technologies(self):
        # Fetch all jobs with an existing tech_stack
        try:
            jobs = Job.query.filter(Job.tech_stack.isnot(None)).all()
            updated_jobs = []

            for job in jobs:
                tech_stack = job.tech_stack  # Get the current tech_stack
                current_app.logger.info(f"Processing job_id: {job.job_id} with tech_stack: {tech_stack}")
                
                if tech_stack:
                    # Parse the tech_stack list and normalize each technology
                    tech_list = [tech.strip().lower() for tech in tech_stack]  # Normalize casing
                    normalized_technologies = set()  # Use a set to avoid duplicates

                    for tech in tech_list:
                        canonical_name = self.normalize_technology_name(tech)
                        if canonical_name:
                            normalized_technologies.add(canonical_name)
                        else:
                            current_app.logger.info(f"Technology '{tech}' could not be normalized")

                    # Clear existing entries in job_technologies for this job
                    JobTechnology.query.filter_by(job_id=job.job_id).delete()
                    db.session.commit()

                    # Insert normalized technologies into job_technologies table
                    for tech_name in normalized_technologies:
                        technology = Technology.query.filter_by(name=tech_name).first()
                        if technology:
                            job_tech = JobTechnology(job_id=job.job_id, technology_id=technology.id)
                            db.session.add(job_tech)

                    db.session.commit()
                    current_app.logger.info(f"Updated job {job.job_id} with normalized technologies: {list(normalized_technologies)}")
                    updated_jobs.append({
                        "job_id": job.job_id,
                        "normalized_technologies": list(normalized_technologies)
                    })

            current_app.logger.info(f"Successfully updated {len(updated_jobs)} jobs")
            return updated_jobs
        except SQLAlchemyError as e:
            current_app.logger.error(f"Database error in update_existing_jobs_technologies: {str(e)}")
            db.session.rollback()
            return []

    def verify_recruiter_email_domain(self, company_id, email):
        company = Company.query.get(company_id)
        if not company:
            return False, "Company not found"
        
        company_domain = self._get_email_domain(company_id)
        recruiter_domain = email.split('@')[-1]
        
        if recruiter_domain.lower() == company_domain.lower():
            return True, "Domain verified"
        else:
            return False, f"Domain mismatch. Expected {company_domain}, got {recruiter_domain}"

    def generate_verification_code(self, recruiter_id):
        recruiter = Recruiter.query.get(recruiter_id)
        if not recruiter:
            return None

        code = ''.join(random.choices('0123456789', k=6))
        recruiter.verification_code = code
        recruiter.verification_code_expiry = datetime.utcnow() + timedelta(minutes=10)
        db.session.commit()

        return code

    def send_verification_email(self, recruiter_id, email):
        code = self.generate_verification_code(recruiter_id)
        if not code:
            return False

        # msg = Message("Verify your email", recipients=[email])
        msg = Message("Please verify your email to complete your onboarding process with OceaniaDevs", recipients=[email])
        msg.body = f"Your verification code is: {code}"
        mail.send(msg)

        return True

    def verify_code(self, recruiter_id, code, company_id):
        recruiter = Recruiter.query.get(recruiter_id)
        if not recruiter:
            return False, "Recruiter not found"

        if recruiter.verification_code != code:
            return False, "Invalid code"

        if datetime.utcnow() > recruiter.verification_code_expiry:
            return False, "Code expired"

        recruiter.email_verified = True
        recruiter.verification_code = None
        recruiter.verification_code_expiry = None

        # Associate recruiter with the company
        company = Company.query.get(company_id)
        
        if company:
            recruiter.company_id = company.company_id
        else:
            return False, "Company not found"

        db.session.commit()

        return True, "Email verified successfully and associated with company"
    
    def has_completed_onboarding(self, recruiter_id):
        recruiter = Recruiter.query.get(recruiter_id)
        if not recruiter:
            return False
        return recruiter.company_id is not None and Company.query.get(recruiter.company_id) is not None

