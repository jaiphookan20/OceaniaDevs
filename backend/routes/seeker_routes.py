from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.seeker_service import SeekerService
from service.jobs_service import JobsService
from models import Seeker, Job
from flask_cors import CORS
from utils.time import get_relative_time
import os
import config
from datetime import datetime

# Create a Blueprint for seeker-related routes
seeker_blueprint = Blueprint('seeker', __name__)
CORS(seeker_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})

# Update Job Seeker Route
@seeker_blueprint.route('/api/update_seeker', methods=['GET', 'POST'])
def update_seeker():
    """
    Route for updating a job seeker's information.

    GET: Renders the 'add_seeker.html' template.
    POST: Extracts form data and calls the 'update_seeker' method of the SeekerService.

    Returns:
        - For GET: Rendered 'add_seeker.html' template.
        - For POST: Success message if the seeker is updated successfully.
        - 401 Unauthorized error if the user is not logged in.
    """
    if request.method == 'POST':
        if 'user' not in session:
            print('user not in session, cannot update Seeker')
            return jsonify({"error": "Unauthorized access"}), 401

        # Extract form data and call the update_seeker method of SeekerService
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        seeker_service = SeekerService()
        seeker_service.update_seeker(first_name, last_name, city, state, country)

        return "Job Seeker Updated successfully!"
    else:
        return render_template('add_seeker.html')

# Get Bookmarked Jobs Route
# @seeker_blueprint.route('/api/bookmarked_jobs')
# def get_all_bookmarked_jobs_by_seeker():
#     if session['user']['type'] != "seeker":
#         return jsonify({"error": "Unauthorized access"}), 401
#     else:
#         seeker_id = session['user']['uid']
#         print(f"seeker_id: {seeker_id}")
#         seeker_service = SeekerService()
#         jobs_service = JobsService()
#         bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)

#         for bookmarked_job in bookmarked_jobs:
#             company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
#             job = jobs_service.get_job_by_id(bookmarked_job.jobid)
#             bookmarked_job.company_name = company.name if company else "N/A"
#             bookmarked_job.title = job.title if job else "N/A"
#             bookmarked_job.city = job.city if job else "N/A"
#             bookmarked_job.state = job.state if job else "N/A"
#             bookmarked_job.country = job.country if job else "N/A"
#             bookmarked_job.salary_range = job.salary_range if job else "N/A"
#             bookmarked_job.specialization = job.specialization if job else "N/A"
#             bookmarked_job.experience_level = job.experience_level if job else "N/A"
#             bookmarked_job.created_at = job.created_at if job else "N/A"
#             bookmarked_job.min_experience_years = job.min_experience_years if job else "N/A"

#             bookmarked_job.logo = company.logo_url;            

#         return jsonify(bookmarked_jobs=[{
#             'job_id': job.jobid,
#             'title': job.title,
#             'company': job.company_name,
#             'city': job.city,
#             'state': job.state,
#             'country': job.country,
#             'experience_level': job.experience_level,
#             'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo)}",
#             'created_at': job.created_at.strftime('%Y-%m-%d'),
#             'specialization': job.specialization,
#             'salary_range': job.salary_range,
#             'min_experience_years': job.min_experience_years,
#         } for job in bookmarked_jobs])

@seeker_blueprint.route('/api/bookmarked_jobs')
def get_all_bookmarked_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        print(f"seeker_id: {seeker_id}")
        
        seeker_service = SeekerService()
        jobs_service = JobsService()
        # bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)
        bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id, page, page_size)

        for bookmarked_job in bookmarked_jobs:
            company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
            job = jobs_service.get_job_by_id(bookmarked_job.jobid)
            bookmarked_job.company_name = company.name if company else "N/A"
            bookmarked_job.company_id = company.company_id if company else "N/A"
            bookmarked_job.title = job.title if job else "N/A"
            bookmarked_job.city = job.city if job else "N/A"
            bookmarked_job.state = job.state if job else "N/A"
            bookmarked_job.country = job.country if job else "N/A"
            bookmarked_job.salary_range = job.salary_range if job else "N/A"
            bookmarked_job.specialization = job.specialization if job else "N/A"
            bookmarked_job.experience_level = job.experience_level if job else "N/A"
            bookmarked_job.created_at = job.created_at if job else "N/A"
            bookmarked_job.min_experience_years = job.min_experience_years if job else "N/A"

            bookmarked_job.logo = company.logo_url;            

        return jsonify(bookmarked_jobs=[{
            'job_id': job.jobid,
            'title': job.title,
            'company': job.company_name,
            'city': job.city,
            'state': job.state,
            'country': job.country,
            'experience_level': job.experience_level,
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo)}",
            'created_at': job.created_at.strftime('%Y-%m-%d'),
            'specialization': job.specialization,
            'salary_range': job.salary_range,
            'min_experience_years': job.min_experience_years,
            'company_id': job.company_id,
        } for job in bookmarked_jobs])

@seeker_blueprint.route('/api/applied_jobs')
def get_all_applied_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        seeker_service = SeekerService()
        jobs_service = JobsService()
        applied_jobs = seeker_service.get_all_applied_jobs_by_seeker(seeker_id)

        applied_jobs_data = []
        for applied_job in applied_jobs:
            company = jobs_service.get_company_by_jobid(applied_job.jobid)
            job = jobs_service.get_job_by_id(applied_job.jobid)
            
            applied_jobs_data.append({
                'job_id': applied_job.jobid,
                'title': job.title if job else "N/A",
                'company': company.name if company else "N/A",
                'city': job.city if job else "N/A",
                'state': job.state if job else "N/A",
                'country': job.country if job else "N/A",
                'experience_level': job.experience_level if job else "N/A",
                'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}" if company and company.logo_url else None,
                'created_at': job.created_at.isoformat() if job and job.created_at else "N/A",
                'specialization': job.specialization if job else "N/A",
                'salary_range': job.salary_range if job else "N/A",
                'applied_at': applied_job.datetimestamp.isoformat(),
                'min_experience_years': job.min_experience_years,
                'status': applied_job.status if hasattr(applied_job, 'status') else 'Applied'
            })

        return jsonify(applied_jobs=applied_jobs_data)

@seeker_blueprint.route('/api/user_applications')
def get_user_applications():
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    seeker_id = session['user']['uid']
    seeker_service = SeekerService()
    jobs_service = JobsService()
    applications = seeker_service.get_all_applied_jobs_by_seeker(seeker_id)

    application_data = []
    for app in applications:
        job = jobs_service.get_job_by_id(app.jobid)
        company = jobs_service.get_company_by_jobid(app.jobid)
        
        application_data.append({
            'id': app.applicationid,
            'company': company.name if company else "N/A",
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}" if company and company.logo_url else None,
            'position': job.title if job else "N/A",
            'appliedDate': app.datetimestamp.strftime('%Y-%m-%d'),
            'status': app.status if hasattr(app, 'status') else 'Applied',
            'jobId': app.jobid
        })

    return jsonify(applications=application_data)


@seeker_blueprint.route('/api/update_application_status/<int:application_id>', methods=['PUT'])
def update_application_status(application_id):
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({"error": "No status provided"}), 400
    
    seeker_service = SeekerService()
    success = seeker_service.update_application_status(application_id, new_status)
    
    if success:
        return jsonify({"message": "Application status updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update application status"}), 500