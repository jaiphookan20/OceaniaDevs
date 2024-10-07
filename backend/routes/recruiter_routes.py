from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app, stream_with_context, Response
from service.recruiter_service import RecruiterService
from service.jobs_service import JobsService
from models import Recruiter, Company, Job
from flask_cors import CORS
from utils.time import get_relative_time
from werkzeug.utils import secure_filename
from datetime import datetime
from utils.time import timing_decorator
import os
import config

recruiter_blueprint = Blueprint('recruiter', __name__)
CORS(recruiter_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost'}})
@recruiter_blueprint.route('/api/job/<int:job_id>', methods=['GET'])
@timing_decorator
def get_job_by_id(job_id):
    try:
        job_service = JobsService()
        job_post = job_service.get_job_by_id(job_id)
        if not job_post:
            current_app.logger.warning(f"Job with id {job_id} not found")
            return jsonify({"error": "Job not found"}), 404
        
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
            "overview": job_post.overview,
            "responsibilities": job_post.responsibilities,
            "requirements": job_post.requirements,
            "company_name": company.name if company else "N/A",
        }
        current_app.logger.info(f"Retrieved job data for job {job_id}")
        return jsonify(job_data)
    except Exception as e:
        current_app.logger.error(f"Error in get_job_by_id: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/companies', methods=['GET'])
@timing_decorator
def get_all_companies():
    try:
        recruiter_service = RecruiterService()
        companies = recruiter_service.get_all_companies()
        current_app.logger.info(f"Retrieved {len(companies)} companies")
        return jsonify(companies), 200
    except Exception as e:
        current_app.logger.error(f"Error in get_all_companies: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/jobs_by_recruiter')
@timing_decorator
def get_all_jobs_by_recruiter():
    try:
        if session['user']['type'] != "recruiter":
            current_app.logger.warning("Unauthorized access attempt in get_all_jobs_by_recruiter")
            return jsonify({"error": "Unauthorized access"}), 401
        
        recruiter_id = session['user']['recruiter_id']
        recruiter_service = RecruiterService()
        jobs_service = JobsService()
        recruiter_jobs = recruiter_service.get_all_jobs_by_recruiter(recruiter_id)
        
        active_jobs = []
        expired_jobs = []
        current_date = datetime.now()
        
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
                "created_at": get_relative_time(job.created_at.strftime('%Y-%m-%d')),
                "updated_at": job.updated_at,
                'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                "company_name": company.name if company else "N/A",
            }
            
            if (current_date - job.created_at).days <= 30:
                active_jobs.append(job_data)
            else:
                expired_jobs.append(job_data)
        
        current_app.logger.info(f"Retrieved {len(active_jobs)} active jobs and {len(expired_jobs)} expired jobs for recruiter {recruiter_id}")
        return jsonify({
            "active_jobs": active_jobs,
            "expired_jobs": expired_jobs
        })
    except Exception as e:
        current_app.logger.error(f"Error in get_all_jobs_by_recruiter: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/recruiter_info', methods=['GET'])
def get_recruiter_info():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in get_recruiter_info")
            return jsonify({"error": "Unauthorized"}), 401

        recruiter_service = RecruiterService()
        recruiter_id = session['user']['recruiter_id']
        recruiter = recruiter_service.get_recruiter_by_id(recruiter_id)
        company = recruiter_service.get_company_by_recruiter_id()

        if not recruiter:
            current_app.logger.warning(f"Recruiter with id {recruiter_id} not found")
            return jsonify({"error": "Recruiter not found"}), 404

        personal_info = {
            "firstName": recruiter.first_name,
            "lastName": recruiter.last_name,
            "email": recruiter.email,
            "position": recruiter.position
        }

        employer_info = {
            "employerName": company.name if company else "",
            "country": company.country if company else "",
            "employerSize": company.size if company else "",
            "website": company.website_url if company else "",
            "address": company.address if company else "",
            "description": company.description if company else "",
            "type": company.type if company else "",
            "city": company.city if company else "",
            "state": company.state if company else "",
            "industry": company.industry if company else "",
            "logo_url": f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}" if company and company.logo_url else ""
        }

        current_app.logger.info(f"Retrieved recruiter info for recruiter {recruiter_id}")
        return jsonify({"personal_info": personal_info, "employer_info": employer_info})
    except Exception as e:
        current_app.logger.error(f"Error in get_recruiter_info: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/update_recruiter_info', methods=['POST'])
def update_recruiter_info():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in update_recruiter_info")
            return jsonify({"error": "Unauthorized"}), 401

        recruiter_service = RecruiterService()
        recruiter_id = session['user']['recruiter_id']
        data = request.json

        # Remove email from the data to be updated
        data.pop('email', None)

        result = recruiter_service.update_recruiter_info(recruiter_id, data)
        if result:
            current_app.logger.info(f"Successfully updated info for recruiter {recruiter_id}")
            return jsonify({"message": "Recruiter info updated successfully"}), 200
        else:
            current_app.logger.warning(f"Failed to update info for recruiter {recruiter_id}")
            return jsonify({"error": "Failed to update recruiter info"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in update_recruiter_info: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/update_recruiter_company', methods=['POST'])
def update_recruiter_company():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in update_recruiter_company")
            return jsonify({"error": "Unauthorized"}), 401

        recruiter_service = RecruiterService()
        recruiter_id = session['user']['recruiter_id']
        
        data = request.form.to_dict()
        logo = request.files.get('logo')

        # Remove employerName from the data to be updated
        data.pop('employerName', None)

        # Ensure description is not longer than 200 characters
        if 'description' in data:
            data['description'] = data['description'][:200]

        result = recruiter_service.update_recruiter_company(recruiter_id, data, logo)
        if result:
            current_app.logger.info(f"Successfully updated company info for recruiter {recruiter_id}")
            return jsonify({"message": "Company info updated successfully"}), 200
        else:
            current_app.logger.warning(f"Failed to update company info for recruiter {recruiter_id}")
            return jsonify({"error": "Failed to update company info"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in update_recruiter_company: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/register/employer/create_company', methods=['POST'])
def create_company():
    try:
        if "user" not in session or session["user"]["type"] != "recruiter":
            current_app.logger.warning("Unauthorized access attempt in create_company")
            return jsonify({"message": "Unauthorized"}), 401

        recruiter_service = RecruiterService()
        recruiter_id = session["user"]["recruiter_id"]
        data = request.form
        logo_file = request.files.get('logo')
        
        result = recruiter_service.create_company(recruiter_id, data, logo_file)
        
        if result:
            current_app.logger.info(f"Successfully created company and updated recruiter {recruiter_id}")
            return jsonify({"message": "Company created and recruiter updated successfully"}), 200
        else:
            current_app.logger.warning(f"Failed to create company or update recruiter {recruiter_id}")
            return jsonify({"message": "Failed to create company or update recruiter"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in create_company: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/process_job_description', methods=['POST'])
def process_job_description():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in process_job_description")
            return jsonify({"error": "Unauthorized access"}), 401

        data = request.json
        description = data.get('description')

        if not description:
            current_app.logger.warning("Job description is required in process_job_description")
            return jsonify({"error": "Job description is required"}), 400

        recruiter_service = RecruiterService()
        processed_description = recruiter_service.process_job_description(description)

        if processed_description:
            current_app.logger.info("Successfully processed job description")
            return jsonify(processed_description), 200
        else:
            current_app.logger.warning("Failed to process job description")
            return jsonify({"error": "Failed to process job description"}), 500
    except Exception as e:
        current_app.logger.error(f"Error in process_job_description: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/process_job_description_with_openai', methods=['POST'])
def process_job_description_with_openai():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in process_job_description_with_openai")
            return jsonify({"error": "Unauthorized access"}), 401

        data = request.json;
        description = data.get('description')
        title = data.get('title')

        if not description:
            current_app.logger.warning("Job description is required in process_job_description_with_openai")
            return jsonify({"error": "Job description is required"}), 400

        recruiter_service = RecruiterService()
        processed_description = recruiter_service.process_job_description_openai(title, description);

        if processed_description:
            current_app.logger.info("Successfully processed job description with OpenAI")
            return jsonify(processed_description), 200
        else:
            current_app.logger.warning("Failed to process job description with OpenAI")
            return jsonify({"error": "Failed to process job description"}), 500
    except Exception as e:
        current_app.logger.error(f"Error in process_job_description_with_openai: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/add_job', methods=['POST'])
def add_job():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in add_job")
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
        specialization=job_data.get('specialization')
        experience_level=job_data.get('experience_level')

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
            specialization,
            experience_level,
            city, 
            state, 
            country, 
            jobpost_url, 
            work_rights
        )

        if new_job:
            current_app.logger.info(f"Successfully added job {new_job.job_id}")
            return jsonify({"message": "Job added successfully", "job_id": new_job.job_id}), 200
        else:
            current_app.logger.warning(f"Failed to add job: {error}")
            return jsonify({"error": f"Failed to add job: {error}"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in add_job: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    try:
        """
        Route for updating an existing job post.
        
        POST: Extracts JSON data and calls the 'update_job' method of the RecruiterService.
        """
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in update_job")
            return jsonify({"error": "Unauthorized access"}), 401
        
        recruiter_id = session['user']['recruiter_id']
        recruiter_service = RecruiterService()
        job_service = JobsService()
        job_post = job_service.get_job_by_id(job_id)

        if not job_post or job_post.recruiter_id != recruiter_id:
            current_app.logger.warning(f"Job {job_id} not found or unauthorized access in update_job")
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
            current_app.logger.info(f"Successfully updated job {job_id}")
            return jsonify({"message": "Job updated successfully"})
        else:
            current_app.logger.warning(f"Job {job_id} not found in update_job")
            return jsonify({"error": "Job not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error in update_job: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/remove-job-by-recruiter/<int:job_id>', methods=['POST'])
def remove_job(job_id):
    try:
        if "user" in session and session["user"]["type"] == "recruiter":
            recruiter_id = session["user"]["recruiter_id"]
            job_service = JobsService()
            recruiter_service = RecruiterService()
            job_post = job_service.get_job_by_id(job_id)

            if not job_post or job_post.recruiter_id != recruiter_id:
                current_app.logger.warning(f"Job {job_id} not found or unauthorized access in remove_job")
                return jsonify({"error": "Job not found or unauthorized"}), 404
            
            if recruiter_service.remove_job(job_id, recruiter_id):
                current_app.logger.info(f"Successfully removed job {job_id}")
                return jsonify({"message": "Job post removed successfully"}), 200
            else:
                current_app.logger.warning(f"Failed to remove job {job_id}")
                return jsonify({"error": "Job not found or unauthorized"}), 404
        else:
            current_app.logger.warning("Unauthorized access attempt in remove_job")
            return jsonify({"message": "Unauthorized"}), 401
    except Exception as e:
        current_app.logger.error(f"Error in remove_job: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/filter-companies', methods=['GET'])
@timing_decorator
def filter_companies():
    try:
        page = int(request.args.get('page', 1))
        page_size = int(request.args.get('page_size', 10))
        search = request.args.get('search', '')
        industries = request.args.get('industries', '').split(',') if request.args.get('industries') else []
        types = request.args.get('types', '').split(',') if request.args.get('types') else []

        current_app.logger.info(f"get_companies search request: {search}")
        current_app.logger.info(f"get_companies industries filter: {industries}")
        current_app.logger.info(f"get_companies types filter: {types}")

        recruiter_service = RecruiterService()
        companies, total_companies = recruiter_service.get_companies_with_pagination(page, page_size, search, industries, types)
        current_app.logger.info(f"get_companies 'companies': {companies}")

        return jsonify({
            'companies': companies,
            'total_companies': total_companies
        })
    except Exception as e:
        current_app.logger.error(f"Error in get_companies: {str(e)}")
        return jsonify({'error': 'An error occurred while fetching companies'}), 500

@recruiter_blueprint.route('/api/company/<int:company_id>', methods=['GET'])
@timing_decorator
def get_company_details(company_id):
    try:
        recruiter_service = RecruiterService()
        company_details = recruiter_service.get_company_details(company_id)
        if company_details:
            current_app.logger.info(f"Retrieved company details for company {company_id}")
            return jsonify(company_details), 200
        else:
            current_app.logger.warning(f"Company {company_id} not found in get_company_details")
            return jsonify({"error": "Company not found"}), 404
    except Exception as e:
        current_app.logger.error(f"Error in get_company_details: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/add_job_ai', methods=['POST'])
def add_job_programmatically():
    try:
        if 'user' not in session or session['user']['type'] != 'recruiter':
            current_app.logger.warning("Unauthorized access attempt in add_job_programmatically")
            return jsonify({"error": "Unauthorized access"}), 401

        recruiter_service = RecruiterService()
        job_data = request.json
        recruiter_id = session['user']['recruiter_id']
        
        # Fetch the recruiter to get the company_id
        recruiter = Recruiter.query.get(recruiter_id)
        if not recruiter or not recruiter.company_id:
            current_app.logger.warning(f"Recruiter {recruiter_id} has not associated with their Company yet in add_job_programmatically")
            return jsonify({"error": "Recruiter has not associated with their Company yet"}), 400

        job_data['recruiter_id'] = recruiter_id
        job_data['company_id'] = recruiter.company_id

        new_job, error = recruiter_service.add_job_programmatically(job_data)

        if new_job:
            current_app.logger.info(f"Successfully added job {new_job.job_id} programmatically")
            return jsonify({"message": "Job added successfully", "job_data": new_job.job_id}), 200
        else:
            current_app.logger.warning(f"Failed to add job programmatically: {error}")
            return jsonify({"error": f"Failed to add job: {error}"}), 400
    except Exception as e:
        current_app.logger.error(f"Error in add_job_programmatically: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/recommended_jobs/<int:job_id>', methods=['GET'])
@timing_decorator
def get_recommended_jobs(job_id):
    try:
        recruiter_service = RecruiterService()
        recommended_jobs = recruiter_service.get_recommended_jobs(job_id)
        current_app.logger.info(f"Retrieved {len(recommended_jobs)} recommended jobs for job {job_id}")
        return jsonify(recommended_jobs)
    except Exception as e:
        current_app.logger.error(f"Error in get_recommended_jobs: {str(e)}")
        return jsonify({"error": "An unexpected error occurred"}), 500

@recruiter_blueprint.route('/api/update-existing-jobs', methods=['POST'])
def update_existing_jobs_technologies():
    try:
        recruiter_service = RecruiterService()
        updated_jobs = recruiter_service.update_existing_jobs_technologies()
        current_app.logger.info(f"Successfully updated {len(updated_jobs)} jobs")
        return jsonify({"success": True, "updated_jobs": updated_jobs}), 200
    except Exception as e:
        current_app.logger.error(f"Error in update_existing_jobs_technologies: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@recruiter_blueprint.route('/api/verify_recruiter_email', methods=['POST'])
def verify_recruiter_email():
    data = request.json
    company_id = data.get('company_id')
    email = data.get('email')

    current_app.logger.info(f"Verifying email: {email} for company_id: {company_id}")

    if not company_id or not email:
        return jsonify({"error": "Missing company_id or email"}), 400

    recruiter_service = RecruiterService()
    is_valid, message = recruiter_service.verify_recruiter_email_domain(company_id, email)

    current_app.logger.info(f"Verification result: {is_valid}, Message: {message}")

    if is_valid:
        recruiter_id = session['user']['recruiter_id']
        try:
            if recruiter_service.send_verification_email(recruiter_id, email):
                return jsonify({"message": "Verification email sent"}), 200
            else:
                return jsonify({"error": "Failed to send verification email"}), 500
        except Exception as e:
            current_app.logger.error(f"Error sending verification email: {str(e)}")
            return jsonify({"error": "Failed to send verification email"}), 500
    else:
        return jsonify({"error": message}), 400

@recruiter_blueprint.route('/api/verify_code', methods=['POST'])
def verify_code():
    data = request.json
    code = data.get('code')
    company_id = data.get('company_id')

    if not code or not company_id:
        return jsonify({"error": "Missing verification code or company ID"}), 400

    recruiter_id = session['user']['recruiter_id']
    recruiter_service = RecruiterService()
    is_valid, message = recruiter_service.verify_code(recruiter_id, code, company_id)

    if is_valid:
        return jsonify({"message": message}), 200
    else:
        return jsonify({"error": message}), 400

@recruiter_blueprint.route('/api/check_onboarding_status', methods=['GET'])
def check_onboarding_status():
    if 'user' not in session or session['user']['type'] != 'recruiter':
        current_app.logger.warning("Unauthorized access attempt in check_onboarding_status")
        return jsonify({"error": "Unauthorized access"}), 401
    
    recruiter_service = RecruiterService()
    recruiter_id = session['user']['recruiter_id']
    
    onboarding_complete = recruiter_service.has_completed_onboarding(recruiter_id)
    return jsonify({"onboardingComplete": onboarding_complete})