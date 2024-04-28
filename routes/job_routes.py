from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.seeker_service import SeekerService
from service.jobs_service import JobsService

job_blueprint = Blueprint('jobs', __name__)

# Apply to Job Route:
@job_blueprint.route('/apply_to_job', methods=['GET', 'POST'])
def apply_to_job():
    userid = request.form['userid']
    jobid = request.form['jobid']

    jobs_service = JobsService()
    jobs_service.apply_to_job(userid, jobid)

    return jsonify({"message": "Job application submitted successfully"})

# Bookmark Job Route:
@job_blueprint.route('/bookmark_job', methods=['POST'])
def bookmark_job():
    userid = request.form['userid']
    jobid = request.form['jobid']

    jobs_service = JobsService()
    jobs_service.bookmark_job(userid, jobid)

    return jsonify({"message": "Job bookmarked successfully"})

# Get all available jobs Route
@job_blueprint.route('/available_jobs')
def available_jobs():
    jobs_service = JobsService()
    jobs = jobs_service.get_available_jobs()
    return render_template('available_jobs.html', jobs=jobs)

# Route to filter jobs based on certain criteria:
@job_blueprint.route('/filter_jobs')
def filter_jobs():
    company_id = request.args.get('company')
    experience_level = request.args.get('experience_level')
    industry = request.args.get('industry')
    
    jobs_service = JobsService()
    filtered_jobs = jobs_service.filter_jobs(company_id, experience_level, industry)
    
    return render_template('filtered_jobs.html', jobs=filtered_jobs)