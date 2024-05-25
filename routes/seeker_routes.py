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


@seeker_blueprint.route('/get_all_applied_jobs_by_seeker')
def get_all_applied_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        print(f"seeker_id: {seeker_id}")
        seeker_service = SeekerService()
        jobs_service = JobsService()
        applied_jobs = seeker_service.get_all_applied_jobs_by_seeker(seeker_id)
        # Fetch company names for each job
        for job in applied_jobs:
            company = jobs_service.get_company_by_id(job.company_id)
            job.company_name = company.name if company else "N/A"
        print(f"recruiter_jobs: {applied_jobs}")
        return render_template('applied_jobs.html', jobs=applied_jobs)