from flask import Blueprint, render_template, request, redirect, url_for, session,jsonify
from service.seeker_service import SeekerService
from service.jobs_service import JobsService
from models import Seeker, Job

seeker_blueprint = Blueprint('seeker', __name__)

# Add Job Seeker Route
@seeker_blueprint.route('/update_seeker', methods=['GET', 'POST'])
def update_seeker():
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


@seeker_blueprint.route('/applied_jobs')
def get_all_applied_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        print(f"seeker_id: {seeker_id}")
        seeker_service = SeekerService()
        jobs_service = JobsService()
        applied_jobs = seeker_service.get_all_applied_jobs_by_seeker(seeker_id)
        bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)
        # Fetch company names for each job
        for applied_job in applied_jobs:
            company = jobs_service.get_company_by_jobid(applied_job.jobid)
            job = jobs_service.get_job_by_id(applied_job.jobid)
            applied_job.company_name = company.name if company else "N/A"
            applied_job.title = job.title if job else "N/A" 
            applied_job.city = job.city if job else "N/A" 
            applied_job.state = job.state if job else "N/A" 
            applied_job.country = job.country if job else "N/A" 
            applied_job.experience_level = job.experience_level if job else "N/A" 
            applied_job.created_at = job.created_at if job else "N/A" 
        return render_template('applied_jobs.html', jobs=applied_jobs)
    
@seeker_blueprint.route('/bookmarked_jobs')
def get_all_bookmarked_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        print(f"seeker_id: {seeker_id}")
        seeker_service = SeekerService()
        jobs_service = JobsService()
        bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)
        # Fetch company names for each job
        for bookmarked_job in bookmarked_jobs:
            company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
            job = jobs_service.get_job_by_id(bookmarked_job.jobid)
            bookmarked_job.company_name = company.name if company else "N/A"
            bookmarked_job.title = job.title if job else "N/A" 
            bookmarked_job.city = job.city if job else "N/A" 
            bookmarked_job.state = job.state if job else "N/A" 
            bookmarked_job.country = job.country if job else "N/A" 
            bookmarked_job.experience_level = job.experience_level if job else "N/A" 
            bookmarked_job.created_at = job.created_at if job else "N/A" 
        return render_template('bookmarked_jobs.html', bookmarked_jobs = bookmarked_jobs)