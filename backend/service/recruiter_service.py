from database import PostgresDB
from extensions import db, bcrypt
from models import Job, Recruiter, Company
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
import time
import config
class RecruiterService:

    def __init__(self):
        self.api_url = "https://api.deepinfra.com/v1/openai/chat/completions"
        self.openai_client = OpenAI(api_key="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")
        self.headers = {
            "Authorization": "Bearer nlcQd4gbjG0eFxxwdXwsIHAKqyIIbcQy",
            "Content-Type": "application/json"
        }
        # Add logging or print statements
        # print("RecruiterService initialized.")
        # current_app.logger.info(f"OpenAI client set: {self.openai_client is not None}")
        # print(f"OpenAI client set: {self.openai_client is not None}")

    def get_recruiter_by_id(self, recruiter_id):
        """
        Return a Recruiter object by the recruiter_id.
        :return: Return a Company object
        """
        return Recruiter.query.get(recruiter_id)
    
    
    # Retrieve all job posts by a Recruiter
    def get_all_jobs_by_recruiter(self, recruiter_id):
        """
        Retrieve all job posts posted by a recruiter.
        :param recruiter_id: int - The ID of the recruiter to fetch.
        """
        # return Job.query.filter_by(recruiter_id=recruiter_id).all()
        return Job.query.filter_by(recruiter_id=recruiter_id).order_by(Job.created_at.desc());

    def get_company_by_recruiter_id(self):
        """
        Retrieve a Company Object using the recruiter's recruiter_id.
        :param recruiter_id: int - The ID of the recruiter associated with the company
        """
        if 'user' not in session or session['user']['type'] != 'recruiter':
            return None
        recruiter_id = session['user']['recruiter_id']
        recruiter = Recruiter.query.get(recruiter_id)
        return Company.query.get(recruiter.company_id) if recruiter else None

    
    # Update Recruiter Personal Data
    # def update_recruiter_info(self, recruiter_id, data):
    #     recruiter = self.get_recruiter_by_id(recruiter_id)
    #     if recruiter:
    #         # for key, value in data.items():
    #         #     setattr(recruiter, key, value)
    #         data = request.get_json()
    #         recruiter.first_name = data.get('firstName')
    #         recruiter.last_name = data.get('lastName')
    #         recruiter.position = data.get('position')
    #         # db.session.commit()
    #         return True
    #     return False

    # def update_recruiter_company(self, recruiter_id, data):
    #     recruiter = self.get_recruiter_by_id(recruiter_id)
    #     if recruiter:
    #         company_name = data.get('company')
    #         current_app.logger.info(f"company_name: {company_name}")
    #         company = Company.query.filter_by(name=company_name).first()
    #         if company:
    #             recruiter.company_id = company.company_id
    #             current_app.logger.info(f"recruiter object: {recruiter}")
    #             # db.session.commit()
    #             return True
    #         else:
    #             current_app.logger.error(f"Company not found: {company_name}")
    #     return False

    def update_recruiter_info(self, recruiter_id, data):
        recruiter = self.get_recruiter_by_id(recruiter_id)
        if recruiter:
            recruiter.first_name = data.get('firstName', recruiter.first_name)
            recruiter.last_name = data.get('lastName', recruiter.last_name)
            recruiter.position = data.get('position', recruiter.position)
            
            try:
                db.session.commit()
                return True
            except Exception as e:
                current_app.logger.error(f"Error updating recruiter info: {str(e)}")
                db.session.rollback()
                return False
        return False

    def update_recruiter_company(self, recruiter_id, data, logo):
        recruiter = self.get_recruiter_by_id(recruiter_id)
        if recruiter and recruiter.company_id:
            company = Company.query.get(recruiter.company_id)
            if company:
                company.country = data.get('country', company.country)
                company.size = data.get('employerSize', company.size)
                company.website_url = data.get('website', company.website_url)
                company.address = data.get('address', company.address)
                company.description = data.get('description', company.description)[:200]
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
                    return True
                except Exception as e:
                    current_app.logger.error(f"Error updating company info: {str(e)}")
                    db.session.rollback()
                    return False
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
            # db.session.rollback()
            return False

    def process_job_description(self, description):
        messages = [
            {
                "role": "system",
                "content": "You are a highly knowledgeable AI assistant specializing in technology job market analysis. Your task is to analyze job descriptions and output structured data in JSON format."
            },
            {
                "role": "user",
                "content": f"""Analyze the following job description and title and provide a response in JSON format with these keys: 'overview', 'responsibilities', 'requirements', 'specialization', 'technologies', 'min_experience_years', 'experience_level', 'industry', 'salary_type', 'salary_range', hourly_range', 'daily_range', 'work_location', 'city', 'state', 'country', 'work_rights', 'job_arrangement, 'contract_duration'.

                Instructions for each key:
                1. 'specialization': Classify the job into ONE of these categories: 'Frontend', 'Backend', 'Cloud & Infrastructure', 'Business Intelligence & Data', 'Machine Learning & AI', 'Full-Stack', 'Mobile', 'Cybersecurity', 'Business Application Development', 'DevOps & IT', 'Project Management', 'QA & Testing'. Note: 'Cloud & Infrastructure' includes Solution Architect roles.
                2. 'technologies': List specific software technologies mentioned (e.g., Java, TypeScript, React, AWS). Exclude general terms like 'LLM services', 'Containers', 'CI/CD' or 'REST APIs'.
                3. 'experience_level': If 'min_experience_years' value is available, classify on basis of the 'min_experience_years' value: if value is between '0-2': 'Junior'; '3-5': 'Mid-Level', '6-10': 'Senior', '10+':'Executive'. If min_experience_years value not available, Classify as you deem fit into one of: 'Junior', 'Mid-Level', 'Senior', or 'Executive'.                

                Important:
                - Provide only the JSON object as output, with no additional text.
                - Ensure all key names are in lowercase.
                - If information for a key is not available, use an empty string or array as appropriate.
                - For 'technologies', use an array of strings, each representing a single technology.

                Job Description: {description}
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
            return processed_data

        except Exception as e:
            current_app.logger.error(f"OpenAI API request failed: {str(e)}")
            return None
        
    def process_job_description_openai(self, title, description):
        messages = [
            {
                "role": "system",
                "content": "You are a highly knowledgeable AI assistant specializing in technology job market analysis. Your task is to analyze job descriptions and output structured data in JSON format."
            },
            {
                "role": "user",
                "content": f"""Analyze the following job description and title and provide a response in JSON format with these keys: 'overview', 'responsibilities', 'requirements', 'specialization', 'technologies', 'min_experience_years', 'experience_level', 'industry', 'salary_type', 'salary_range', hourly_range', 'daily_range', 'work_location', 'city', 'state', 'country', 'work_rights', 'job_arrangement, 'contract_duration'.

                Instructions for each key:
                1. 'overview': Summarize the role and company, including all key and salient information relevant to potential candidates. Add any information related to benefits or perks here. Add information verbatim if needed but all of the information is needed.
                2. 'min_experience_years': Extract the highest number of years of experience mentioned for any skill. Only if mentioned. Otherwise, leave empty.
                3. 'industry': Identify the end market or industry of the client that the role serves. If client is federal government, industry = 'government'. Use one of the following: ['Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics'].
                4. 'responsibilities': List main job duties and expectations. 
                5. 'requirements': Enumerate essential qualifications and skills needed.
                6. 'specialization': Classify the job into ONLY ONE of these categories: 'Frontend', 'Backend', 'Cloud & Infrastructure', 'Business Intelligence & Data', 'Machine Learning & AI', 'Full-Stack', 'Mobile', 'Cybersecurity', 'Business Application Development', 'DevOps & IT', 'Project Management', 'QA & Testing'. Note: 'Cloud & Infrastructure' includes Solution Architect roles. You cannot select any other category other than the ones listed.
                7. 'technologies': List specific software technologies mentioned (e.g., Java, TypeScript, React, AWS). Exclude general terms like 'LLM services', 'Containers', 'CI/CD' or 'REST APIs'.
                8. 'experience_level': If 'min_experience_years' value is available, classify on basis of the 'min_experience_years' value: if value is between '0-2': 'Junior'; '3-5': 'Mid-Level', '6-10': 'Senior', '10+':'Executive'. If min_experience_years value not available, Classify as you deem fit into one of: 'Junior', 'Mid-Level', 'Senior', or 'Executive'.                
                9. 'salary_type': If only available, specify the type of salary or payment arrangement (e.g., 'Annual', 'Hourly', 'Daily').
                10. 'salary_range': If only available AND salary_type="Annual", extract the salary information and classify it in the bucket it fits in: '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+'. Otherwise leave empty.
                11. 'hourly_range': If only available AND salary_type="Hourly", extract the hourly-rate information and classify it in the bucket it fits in: '0 - 20', '20 - 30', '30 - 40', '40 - 50', '50 - 60', '60 - 70', '70 - 80', '80 - 100', '100+'. Otherwise leave empty.
                12. 'daily_range': If only available AND salary_type="Daily", extract the daily-rate information and classify it in the bucket it fits in: '300 - 400', '400 - 500', '500 - 600', '600 - 700', '700 - 800', '800 - 900', '900 - 1000', '1000 - 1100', '1200+'. Otherwise leave empty.
                13. 'work_location': Specify the work location as one of: 'Remote', 'Hybrid', 'Office'. Default option: 'Office'.
                14. 'city': Extract the city where the job is located. Strictly only do so if mentioned, otherwise empty.
                15. 'state': Extract the state where the job is located. Use one of the following: ['VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA']. Strictly only do so if mentioned, otherwise empty.
                16. 'country': Extract the country where the job is located. Use one of the following: ['Australia', 'New Zealand'].
                17. 'work_rights': List any work rights or visa requirements. Strictly only do so if mentioned, otherwise empty.
                18. 'job_arrangement': Specify the job arrangement as one of: 'Permanent', 'Contract', 'Internship'.
                19. 'contract_duration': If only the 'job_arrangement' is 'Contract', and if the duration of the contract is provided and available, classify it as belonging to one of the following buckets: '3-6 Months', '6-9 Months', '9-12 Months' or '12 Months+'. Otherwise leave empty.

                Important:
                - Provide only the JSON object as output, with no additional text.
                - Ensure all key names are in lowercase.
                - If information for a key is not available, use an empty string or array as appropriate.
                - For 'responsibilities' and 'requirements', use arrays of strings.
                - For 'technologies', use an array of strings, each representing a single technology.

                Title: {title}
                Job Description: {description}
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
            return processed_data

        except Exception as e:
            current_app.logger.error(f"OpenAI API request failed: {str(e)}")
            return None
    
    # Add Job
    def add_job(self, recruiter_id, company_id, title, description, job_type, industry, salary_range, salary_type, work_location, min_experience_years, city, state, country, jobpost_url, work_rights, specialization, experience_level, tech_stack):
        if session['user']['type'] != "recruiter":
            return None, "Unauthorized access"

        try:
            # processed_data = self.process_job_description(description)

            new_job = Job(
                    recruiter_id=recruiter_id,
                    company_id=company_id,
                    title=title,
                    description=description,
                    specialization=specialization,
                    job_type=job_type,
                    industry=industry,
                    salary_range=salary_range,
                    salary_type=salary_type,
                    work_location=work_location,
                    min_experience_years=min_experience_years,
                    experience_level=experience_level,
                    city=city,
                    state=state,
                    country=country,
                    jobpost_url=jobpost_url,
                    work_rights=work_rights,
                    tech_stack=tech_stack);
            db.session.add(new_job)
            db.session.commit()
            return new_job, None
        
        except Exception as e:
            db.session.rollback()
            current_app.logger.error(f"Error adding job: {str(e)}")
            return None, f"An error occurred while adding the job: {str(e)}"    
    
    # Add Job with AI
    def add_job_programmatically(self, job_data):
        try:
            title = job_data.get('title')
            description = job_data.get('description')

            with concurrent.futures.ThreadPoolExecutor() as executor:
                future = executor.submit(self.process_job_description_openai, title, description)
                try:
                    processed_data = future.result(timeout=180)  # 3 minutes timeout
                except TimeoutError:
                    return None, "OpenAI API call timed out after 3 minutes"

            current_app.logger.info(f"Processed Data: {processed_data}")

            if processed_data:
                new_job = Job(
                    recruiter_id=job_data.get('recruiter_id'),
                    company_id=job_data.get('company_id'),
                    title=title,
                    description=description,
                    jobpost_url=job_data.get('jobpost_url'),
                    specialization=job_data.get('specialization') or processed_data.get('specialization'),
                    industry=job_data.get('industry') or processed_data.get('industry'),
                    salary_range=job_data.get('salary_range') or processed_data.get('salary_range') or '80000 - 100000',
                    salary_type=job_data.get('salary_type') or processed_data.get('salary_type'),
                    work_location=job_data.get('work_location') or processed_data.get('work_location'),
                    min_experience_years=job_data.get('min_experience_years') or processed_data.get('min_experience_years') or 0,
                    experience_level=job_data.get('experience_level') or processed_data.get('experience_level'),
                    city=job_data.get('city') or processed_data.get('city'),
                    state=job_data.get('state') or processed_data.get('state'),
                    country=job_data.get('country') or processed_data.get('country'),
                    work_rights=job_data.get('work_rights') or processed_data.get('work_rights'),
                    tech_stack=job_data.get('tech_stack') or processed_data.get('technologies'),
                    overview=processed_data.get('overview') or processed_data.get('overview'),
                    responsibilities=job_data.get('responsibilities', '') or processed_data.get('responsibilities'),
                    requirements=job_data.get('requirements', '') or processed_data.get('requirements'),
                    job_arrangement=job_data.get('job_arrangement') or processed_data.get('job_arrangement'),
                    contract_duration=job_data.get('contract_duration') or processed_data.get('contract_duration'),
                    hourly_range=job_data.get('hourly_range') or processed_data.get('hourly_range'),
                    daily_range=job_data.get('daily_range') or processed_data.get('daily_range'),
                )
                
                current_app.logger.info(new_job)
                # db.session.add(new_job)
                # db.session.commit()

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
    
    def get_all_companies(self):
        companies = Company.query.all()
        return [{
            "company_id": company.company_id,
            "name": company.name,
            "description": company.description,
            "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
            "size": company.size,
            "address": company.address,
            "job_count": self.get_job_count_for_company(company.company_id)
        } for company in companies]

    # def get_companies_with_pagination(self, page, page_size, search):
    #     query = Company.query

    #     current_app.logger.info(f"Search query: {search}")

    #     if search:
    #         query = query.filter(Company.name.ilike(f'%{search}%'))
    #         current_app.logger.info(f"Filtered query: {query}")

    #     total_companies = query.count()
    #     current_app.logger.info(f"Total companies after filter: {total_companies}")

    #     companies = query.order_by(Company.name).paginate(page=page, per_page=page_size, error_out=False).items

    #     return [{
    #         "company_id": company.company_id,
    #         "name": company.name,
    #         "description": company.description,
    #         "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
    #         "address": company.address,
    #         "city": company.city,
    #         "state": company.state,
    #         "industry": company.industry,
    #         "type": company.type,
    #         "job_count": self.get_job_count_for_company(company.company_id)
    #     } for company in companies], total_companies

    # In recruiter_service.py

    def get_companies_with_pagination(self, page, page_size, search, industries, types):
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

        return [{
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
        } for company in companies], total_companies 


    def get_job_count_for_company(self, company_id):
        return Job.query.filter_by(company_id=company_id).count()
    
    def get_company_details(self, company_id):
        company = Company.query.get(company_id)
        if not company:
            return None
        
        jobs = Job.query.filter_by(company_id=company_id).all()
        job_count = len(jobs)

        # Collect and de-duplicate tech stack
        tech_stack = []
        for job in jobs:
            if job.tech_stack:  # Check if tech_stack is not None
                tech_stack.extend(job.tech_stack)

        # Remove duplicates and sort
        unique_tech_stack = sorted(set(tech_stack))
        
        return {
            "company_id": company.company_id,
            "name": company.name,
            "description": company.description,
            "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
            "size": company.size,
            "website_url": company.website_url,
            "total_jobs": job_count,
            "address": company.address,
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
            } for job in jobs],
        }
    
    def get_recommended_jobs(self, job_id):
        current_job = Job.query.get(job_id)
        if not current_job:
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
                "location": f"{job.city}, {job.state}, {job.country}",
                "salary_range": job.salary_range,
                "experience_level": job.experience_level,
                'specialization': job.specialization,
                'min_experience_years': job.min_experience_years,
                "created_at": get_relative_time(job.created_at.strftime("%Y-%m-%d"))
            })
        
        return result

    
    # def extract_text_from_pdf(self, pdf_file):
    #     try:
    #         pdf_reader = PyPDF2.PdfReader(pdf_file)
    #         text = ""
    #         for page in pdf_reader.pages:
    #             text += page.extract_text()
    #         return text
    #     except Exception as e:
    #         current_app.logger.error(f"Error extracting text from PDF: {str(e)}")
    #         return None

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
            return processed_data

        except Exception as e:
            current_app.logger.error(f"OpenAI API request failed: {str(e)}")
            return None
                
    def process_jobs_from_json(self):
        current_dir = os.path.dirname(os.path.abspath(__file__))
        input_file_path = os.path.join(current_dir, 'jobs.json')
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