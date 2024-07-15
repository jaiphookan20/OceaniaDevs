from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.seeker_service import SeekerService
from service.jobs_service import JobsService
from models import Seeker, Job
from flask_cors import CORS
from utils.time import get_relative_time
import os
import config
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
@seeker_blueprint.route('/api/bookmarked_jobs')
def get_all_bookmarked_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        print(f"seeker_id: {seeker_id}")
        seeker_service = SeekerService()
        jobs_service = JobsService()
        bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)

        for bookmarked_job in bookmarked_jobs:
            company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
            job = jobs_service.get_job_by_id(bookmarked_job.jobid)
            bookmarked_job.company_name = company.name if company else "N/A"
            bookmarked_job.title = job.title if job else "N/A"
            bookmarked_job.city = job.city if job else "N/A"
            bookmarked_job.state = job.state if job else "N/A"
            bookmarked_job.country = job.country if job else "N/A"
            bookmarked_job.salary_range = job.salary_range if job else "N/A"
            bookmarked_job.specialization = job.specialization if job else "N/A"
            bookmarked_job.experience_level = job.experience_level if job else "N/A"
            bookmarked_job.created_at = job.created_at if job else "N/A"


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
            'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
            'specialization': job.specialization,
            'salary_range': job.salary_range
        } for job in bookmarked_jobs])
    

# Get Applied Jobs Route
@seeker_blueprint.route('/api/applied_jobs')
def get_all_applied_jobs_by_seeker():
    """
    Route for retrieving all jobs applied by a job seeker.

    Returns:
        - Rendered 'applied_jobs.html' template with a list of applied jobs.
        - 401 Unauthorized error if the user is not a seeker.
    """
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        print(f"seeker_id: {seeker_id}")
        seeker_service = SeekerService()
        jobs_service = JobsService()
        applied_jobs = seeker_service.get_all_applied_jobs_by_seeker(seeker_id)

        # Fetch company names and job details for each applied job
        for applied_job in applied_jobs:
            company = jobs_service.get_company_by_jobid(applied_job.jobid)
            job = jobs_service.get_job_by_id(applied_job.jobid)
            applied_job.company_name = company.name if company else "N/A"
            applied_job.title = job.title if job else "N/A"
            applied_job.city = job.city if job else "N/A"
            applied_job.state = job.state if job else "N/A"
            applied_job.country = job.country if job else "N/A"
            applied_job.experience_level = job.experience_level if job else "N/A"
            applied_job.specialization = job.specialization if job else "N/A"
            applied_job.salary_range = job.salary_range if job else "N/A"
            applied_job.created_at = job.created_at if job else "N/A"
            applied_job.logo = company.logo_url if job else "N/A"

        return jsonify(applied_jobs=[{
            'job_id': job.jobid,
            'title': job.title,
            'company': job.company_name,
            'city': job.city,
            'state': job.state,
            'country': job.country,
            'experience_level': job.experience_level,
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo)}",
            'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
            'specialization': job.specialization,
            'salary_range': job.salary_range
        } for job in applied_jobs])