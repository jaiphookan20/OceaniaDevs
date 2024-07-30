from database import PostgresDB
from extensions import db, bcrypt
from models import Job, Recruiter, Company
from flask import session, jsonify, current_app, request
from utils.categorize import categorize_words
import requests
import json
from werkzeug.utils import secure_filename
import os
class RecruiterService:

    def __init__(self):
        self.api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.headers = {
            "Authorization": "Bearer nlcQd4gbjG0eFxxwdXwsIHAKqyIIbcQy",
            "Content-Type": "application/json"
        }

    def get_recruiter_by_id(self, recruiter_id):
        """
        Return a Recruiter object by the recruiter_id.
        :return: Return a Company object
        """
        return Recruiter.query.get(recruiter_id)
    
    def get_all_companies(self):
        companies = Company.query.all()
        return [{"name": company.name} for company in companies]
    
    # Retrieve all job posts by a Recruiter
    def get_all_jobs_by_recruiter(self, recruiter_id):
        """
        Retrieve all job posts posted by a recruiter.
        :param recruiter_id: int - The ID of the recruiter to fetch.
        """
        return Job.query.filter_by(recruiter_id=recruiter_id).all()

    # def get_company_by_recruiter_id(self):
    #     """
    #     Retrieve a Company Object using the recruiter's recruiter_id.
    #     :param recruiter_id: int - The ID of the recruiter associated with the company
    #     """
    #     if (session.get('user').get('type') != 'recruiter'):
    #         return jsonify({"error": "Unauthorized access. Only Recruiters can access this resource"}), 401
    #     recruiter_id = session['user']['recruiter_id'];
    #     recruiter = Recruiter.query.get(recruiter_id);
    #     company = Company.query.get(recruiter.company_id)
    #     print(f"Inside recruiter service: company: {company}")
    #     if not company:
    #         return None
    #     return company;
    
    # Add a Job Post to the Jobs table
    # def add_job(self, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, city, state, country, jobpost_url, work_rights):
    #     """
    #     Add a Job Post to the Jobs table.
    #     """
    #     if session['user']['type'] != "recruiter":
    #         return None, "Unauthorized access"
    
    #     try:
    #         new_job = Job(
    #             recruiter_id=recruiter_id,
    #             company_id=company_id,
    #             title=title,
    #             description=description,
    #             specialization=specialization,
    #             job_type=job_type,
    #             industry=industry,
    #             salary_range=salary_range,
    #             salary_type=salary_type,
    #             work_location=work_location,
    #             min_experience_years=min_experience_years,
    #             experience_level=experience_level,
    #             city=city,
    #             state=state,
    #             country=country,
    #             jobpost_url=jobpost_url,
    #             work_rights=work_rights
    #         )
    #         db.session.add(new_job)
    #         db.session.commit()

    #         # Categorize the job description and update the tech_stack
    #         categorized_tech_stack = categorize_words(new_job.description)
    #         new_job.tech_stack = categorized_tech_stack
    #         db.session.commit()

    #         return new_job, None  # Return the job object and no error
    #     except Exception as e:
    #         db.session.rollback()
    #         return None, str(e)  # Return None for the job and the error message

    # Update Recruiter Personal Data
    def update_recruiter_info(self, recruiter_id, data):
        recruiter = self.get_recruiter_by_id(recruiter_id)
        if recruiter:
            # for key, value in data.items():
            #     setattr(recruiter, key, value)
            data = request.get_json()
            recruiter.first_name = data.get('firstName')
            recruiter.last_name = data.get('lastName')
            recruiter.position = data.get('position')
            db.session.commit()
            return True
        return False

    def update_recruiter_company(self, recruiter_id, data):
        recruiter = self.get_recruiter_by_id(recruiter_id)
        if recruiter:
            company = Company.query.filter_by(name=data.get('company')).first() # This could potentially cause errors later, better to filter by the company_id. We are only sending the company_name from the frontend
            if company:
                recruiter.company_id = company.company_id
                db.session.commit()
                return True
        return False
        
    def create_company(self, recruiter_id, data, logo_file):
        try:
            logo_path = None
            if logo_file:
                logo_filename = secure_filename(logo_file.filename)
                logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename)
                logo_file.save(logo_path)

            name = data.get('employerName');
            website_url= data.get('employerWebsite');
            country= data.get('country');
            size = data.get('employerSize');
            address= data.get('employerAddress');
            description= data.get('employerDescription');
            logo_url= logo_path;
            
            new_company = Company(
                name=name,
                website_url=website_url,
                country = country,
                size = size,
                address = address,
                description = description,
                logo_url = logo_url
            )

            db.session.add(new_company)
            db.session.commit()

            recruiter = self.get_recruiter_by_id(recruiter_id)
            recruiter.company_id = new_company.company_id
            db.session.commit()

            return True
        except Exception as e:
            print('Exception in create_company');
            print(e);
            db.session.rollback()
            return False

    def process_job_description(self, description):
        messages = [
            {
                "role": "user",
                "content": f"""Analyze the following job description and provide a response in JSON format with the following keys: 'overview', 'specialization', 'technologies', 'experience_level', 'responsibilities', 'requirements'.
            
            For the specialization, classify the job into one of the following: 'frontend', 'backend', 'cloud & infra', 'business intelligence & data', 'machine learning & AI', 'full-stack', 'mobile', 'Cybersecurity', 'Business Application Development', 'DevOps & IT'. 
            Choose only one that most closely matches the job post.

            For technologies, extract specific proprietary software technologies mentioned in the job post (e.g., Java, TypeScript, React, AWS). Do not include general terms like 'LLM services', 'Containers', or 'CI/CD'.

            For experience_level, classify as one of: Junior, Associate, Mid-Level, Senior, or Leadership.
            Strictly follow this: Do not provide anything other than the JSON response output. Provide it as a JSON object only.
            Job Description:{description}
            """
            }
        ]

        payload = {
            "model": "meta-llama/Meta-Llama-3-70B-Instruct",
            "messages": messages,
            "temperature": 0.7,
            "max_tokens": 2000,
            "response_format": {"type": "json_object"}
        }

        try:
            response = requests.post(self.api_url, headers=self.headers, json=payload)
            response.raise_for_status()
            result = response.json()
            
            current_app.logger.info(f"API Response: {result}")
            
            content = result['choices'][0]['message']['content']
            current_app.logger.info(f"Extracted content: {content}")
            
            content = content.strip().strip('"').replace('\\n', '\n')
            processed_data = json.loads(content)
            return processed_data
            
        except requests.exceptions.RequestException as e:
            current_app.logger.error(f"API request failed: {str(e)}")
            return None
        except json.JSONDecodeError as e:
            current_app.logger.error(f"JSON parsing error: {str(e)}")
            current_app.logger.error(f"Raw content: {content}")
            return None
        except Exception as e:
            current_app.logger.error(f"Unexpected error: {str(e)}")
            return None

    # Add Job
    def add_job(self, recruiter_id, company_id, title, description, job_type, industry, salary_range, salary_type, work_location, min_experience_years, city, state, country, jobpost_url, work_rights):
        if session['user']['type'] != "recruiter":
            return None, "Unauthorized access"

        try:
            processed_data = self.process_job_description(description)

            if processed_data:
                new_job = Job(
                    recruiter_id=recruiter_id,
                    company_id=company_id,
                    title=title,
                    description=description,
                    specialization=processed_data.get('specialization', []),
                    job_type=job_type,
                    industry=industry,
                    salary_range=salary_range,
                    salary_type=salary_type,
                    work_location=work_location,
                    min_experience_years=min_experience_years,
                    experience_level=processed_data.get('experience_level', []),
                    city=city,
                    state=state,
                    country=country,
                    jobpost_url=jobpost_url,
                    work_rights=work_rights,
                    tech_stack=processed_data.get('technologies', [])
                )

                db.session.add(new_job)
                db.session.commit()

                return new_job, None
            else:
                return None, "Failed to process job description"

        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding job: {str(e)}")
            return None, f"An error occurred while adding the job: {str(e)}"
        
    # Update a job post with given updates
    def update_job(self, job_id, data):
        """
        Update a job post with given updates.
        :param job_id: int - The ID of the job to be updated.
        :param data: dict - A dictionary containing the fields to update with their new values.
        """
        job = Job.query.get(job_id)
        if not job:
            return None
        
        for key, value in data.items():
            setattr(job, key, value)
        
        db.session.commit()
        return job
    
    def remove_job(self, job_id, recruiter_id):
        job = Job.query.filter_by(job_id=job_id, recruiter_id=recruiter_id).first()
        if job:
            db.session.delete(job)
            db.session.commit()
            return True
        return False