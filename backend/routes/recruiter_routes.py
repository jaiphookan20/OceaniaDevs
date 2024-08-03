from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from service.recruiter_service import RecruiterService
from service.jobs_service import JobsService
from models import Recruiter, Company, Job
from extensions import db
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os
import config


# Create a Blueprint for recruiter-related routes
recruiter_blueprint = Blueprint('recruiter', __name__)
CORS(recruiter_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost'}})

# Add Recruiter Route
@recruiter_blueprint.route('/api/add_recruiter', methods=['GET', 'POST'])
    
# Get Job Details by Job ID
@recruiter_blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    job_service = JobsService()
    job_post = job_service.get_job_by_id(job_id)
    if job_post:
        company = job_service.get_company_by_id(job_post.company_id)
        job_data = {
            "job_id": job_post.job_id,
            "recruiter_id": job_post.recruiter_id,
            "company_id": job_post.company_id,
            "title": job_post.title,
            "description": job_post.description,
            "specialization": job_post.specialization,
            "job_type": job_post.job_type,
            "industry": job_post.industry,
            "salary_range": job_post.salary_range,
            "salary_type": job_post.salary_type,
            "work_location": job_post.work_location,
            "min_experience_years": job_post.min_experience_years,
            "experience_level": job_post.experience_level,
            "tech_stack": job_post.tech_stack,
            "city": job_post.city,
            "state": job_post.state,
            "country": job_post.country,
            "expiry_date": job_post.expiry_date,
            "jobpost_url": job_post.jobpost_url,
            "work_rights": job_post.work_rights,
            "created_at": job_post.created_at,
            "updated_at": job_post.updated_at,
            "company_name": company.name if company else "N/A",
        }
        return jsonify(job_data)
    else:
        return jsonify({"error": "Job not found"}), 404

# Get All Companies Objects
@recruiter_blueprint.route('/api/companies', methods=['GET'])
def get_all_companies():
    recruiter_service = RecruiterService()
    companies = recruiter_service.get_all_companies()
    return jsonify(companies), 200

# Get All Jobs Posted by the Recruiter
@recruiter_blueprint.route('/api/jobs_by_recruiter')
def get_all_jobs_by_recruiter():
    if session['user']['type'] != "recruiter":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        recruiter_id = session['user']['recruiter_id']
        recruiter_service = RecruiterService()
        jobs_service = JobsService()
        recruiter_jobs = recruiter_service.get_all_jobs_by_recruiter(recruiter_id)
        # Build the response data
        response_data = []
        for job in recruiter_jobs:
            company = jobs_service.get_company_by_id(job.company_id)

            job_data = {
                "job_id": job.job_id,
                "recruiter_id": job.recruiter_id,
                "company_id": job.company_id,
                "title": job.title,
                "description": job.description,
                "specialization": job.specialization,
                "job_type": job.job_type,
                "industry": job.industry,
                "salary_range": job.salary_range,
                "salary_type": job.salary_type,
                "work_location": job.work_location,
                "min_experience_years": job.min_experience_years,
                "experience_level": job.experience_level,
                "tech_stack": job.tech_stack,
                "city": job.city,
                "state": job.state,
                "country": job.country,
                "expiry_date": job.expiry_date,
                "jobpost_url": job.jobpost_url,
                "work_rights": job.work_rights,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
                'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                "company_name": company.name if company else "N/A",
            }
            response_data.append(job_data)
        
        return jsonify(response_data)

# -------------------------END OF GET REQUESTS-------------------------------

# Update Recruiter Personal Data
@recruiter_blueprint.route('/api/register/employer/info', methods=['POST'])
def update_recruiter_info():
    if "user" not in session or session["user"]["type"] != "recruiter":
        return jsonify({"message": "Unauthorized"}), 401

    recruiter_service = RecruiterService()
    recruiter_id = session["user"]["recruiter_id"]
    data = request.get_json()
    
    result = recruiter_service.update_recruiter_info(recruiter_id, data)
    
    if result:
        return jsonify({"message": "Recruiter info updated successfully"}), 200
    else:
        return jsonify({"message": "Recruiter not found"}), 404

@recruiter_blueprint.route('/api/register/employer/update_company', methods=['POST'])
def update_recruiter_company():
    if "user" not in session or session["user"]["type"] != "recruiter":
        return jsonify({"message": "Unauthorized"}), 401

    recruiter_service = RecruiterService()
    recruiter_id = session["user"]["recruiter_id"]
    data = request.get_json()
    
    result = recruiter_service.update_recruiter_company(recruiter_id, data)
    
    if result:
        return jsonify({"message": "Recruiter company updated successfully"}), 200
    else:
        return jsonify({"message": "Company not found or Recruiter not found"}), 404
    
# Create Recruiter's Company if Company not present in DB
@recruiter_blueprint.route('/api/register/employer/create_company', methods=['POST'])
def create_company():
    if "user" not in session or session["user"]["type"] != "recruiter":
        return jsonify({"message": "Unauthorized"}), 401

    recruiter_service = RecruiterService()
    recruiter_id = session["user"]["recruiter_id"]
    data = request.form
    logo_file = request.files.get('logo')
    
    result = recruiter_service.create_company(recruiter_id, data, logo_file)
    
    if result:
        return jsonify({"message": "Company created and recruiter updated successfully"}), 200
    else:
        return jsonify({"message": "Failed to create company or update recruiter"}), 400
    
@recruiter_blueprint.route('/api/process_job_description', methods=['POST'])
def process_job_description():
    # if 'user' not in session or session['user']['type'] != 'recruiter':
    #     return jsonify({"error": "Unauthorized access"}), 401

    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "Job description is required"}), 400

    recruiter_service = RecruiterService()
    processed_description = recruiter_service.process_job_description(description)

    if processed_description:
        return jsonify(processed_description), 200
    else:
        return jsonify({"error": "Failed to process job description"}), 500
    
@recruiter_blueprint.route('/api/process_job_description_with_openai', methods=['POST'])
def process_job_description_with_openai():
    # if 'user' not in session or session['user']['type'] != 'recruiter':
    #     return jsonify({"error": "Unauthorized access"}), 401

    data = request.json
    description = data.get('description')

    if not description:
        return jsonify({"error": "Job description is required"}), 400

    recruiter_service = RecruiterService()
    processed_description = recruiter_service.process_job_description_openai(description)

    if processed_description:
        return jsonify(processed_description), 200
    else:
        return jsonify({"error": "Failed to process job description"}), 500

# Add Job Route
@recruiter_blueprint.route('/api/add_job', methods=['POST'])
def add_job():
    if 'user' not in session or session['user']['type'] != 'recruiter':
        return jsonify({"error": "Unauthorized access"}), 401

    recruiter_service = RecruiterService()
    job_data = request.json
    job_data['recruiter_id'] = session['user']['recruiter_id']

    # Extract individual fields from job_data
    recruiter_id = job_data.get('recruiter_id')
    company_id = job_data.get('company_id')
    title = job_data.get('title')
    description = job_data.get('description')
    job_type = job_data.get('job_type')
    industry = job_data.get('industry')
    salary_range = job_data.get('salary_range')
    salary_type = job_data.get('salary_type')
    work_location = job_data.get('work_location')
    min_experience_years = job_data.get('min_experience_years')
    city = job_data.get('city')
    state = job_data.get('state')
    country = job_data.get('country')
    jobpost_url = job_data.get('jobpost_url')
    work_rights = job_data.get('work_rights')

    # Call the service method with individual arguments
    new_job, error = recruiter_service.add_job(
        recruiter_id, 
        company_id, 
        title, 
        description, 
        job_type, 
        industry, 
        salary_range, 
        salary_type, 
        work_location, 
        min_experience_years, 
        city, 
        state, 
        country, 
        jobpost_url, 
        work_rights
    )

    if new_job:
        return jsonify({"message": "Job added successfully", "job_id": new_job.job_id}), 200
    else:
        return jsonify({"error": f"Failed to add job: {error}"}), 400
    
# Update Job Route
@recruiter_blueprint.route('/api/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    """
    Route for updating an existing job post.
    
    POST: Extracts JSON data and calls the 'update_job' method of the RecruiterService.
    """
    if 'user' not in session or session['user']['type'] != 'recruiter':
        return jsonify({"error": "Unauthorized access"}), 401
    
    recruiter_id = session['user']['recruiter_id']
    recruiter_service = RecruiterService()
    job_service = JobsService()
    job_post = job_service.get_job_by_id(job_id)

    if not job_post or job_post.recruiter_id != recruiter_id:
        return jsonify({"error": "Job not found or unauthorized"}), 404

    data = request.get_json()
    updated_data = {
        'title': data['title'],
        'description': data['description'],
        'specialization': data['specialization'],
        'job_type': data['job_type'],
        'industry': data['industry'],
        'salary_range': data['salary_range'],
        'salary_type': data['salary_type'],
        'work_location': data['work_location'],
        'min_experience_years': data['min_experience_years'],
        'experience_level': data['experience_level'],
        'tech_stack': data['tech_stack'],
        'city': data['city'],
        'state': data['state'],
        'country': data['country'],
        'jobpost_url': data['jobpost_url'],
        'work_rights': data['work_rights']
    }
    updated_job = recruiter_service.update_job(job_id, updated_data)
    if updated_job:
        return jsonify({"message": "Job updated successfully"})
    else:
        return jsonify({"error": "Job not found"}), 404
    
# Remove Job Post of a Recruiter
@recruiter_blueprint.route('/api/remove-job-by-recruiter/<int:job_id>', methods=['POST'])
def remove_job(job_id):
    if "user" in session and session["user"]["type"] == "recruiter":
        recruiter_id = session["user"]["recruiter_id"]
        job_service = JobsService()
        recruiter_service = RecruiterService()
        job_post = job_service.get_job_by_id(job_id)

        if not job_post or job_post.recruiter_id != recruiter_id:
            return jsonify({"error": "Job not found or unauthorized"}), 404
        
        if recruiter_service.remove_job(job_id, recruiter_id):
            return jsonify({"message": "Job post removed successfully"}), 200
        else:
            return jsonify({"error": "Job not found or unauthorized"}), 404
    else:
        return jsonify({"message": "Unauthorized"}), 401


@recruiter_blueprint.route('/api/companies', methods=['GET'])
def get_companies():
    page = int(request.args.get('page', 1))
    page_size = int(request.args.get('page_size', 10))
    search = request.args.get('search', '')

    recruiter_service = RecruiterService()
    companies, total_companies = recruiter_service.get_companies_with_pagination(page, page_size, search)

    return jsonify({
        'companies': companies,
        'total_companies': total_companies
    })

@recruiter_blueprint.route('/api/company/<int:company_id>', methods=['GET'])
def get_company_details(company_id):
    recruiter_service = RecruiterService()
    company_details = recruiter_service.get_company_details(company_id)
    if company_details:
        return jsonify(company_details), 200
    else:
        return jsonify({"error": "Company not found"}), 404