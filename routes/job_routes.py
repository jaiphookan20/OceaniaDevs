from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from service.seeker_service import SeekerService
from service.jobs_service import JobsService

job_blueprint = Blueprint('jobs', __name__)

# Apply to Job Route:
@job_blueprint.route('/apply_to_job', methods=['GET', 'POST'])
def apply_to_job():
    if 'user_id' not in session:
        print('user not in session!')
        return jsonify({"error": "Unauthorized access"}), 401

    job_id = request.json['jobid']
    if type(job_id) is not int:
        print("Invalid job id: ")
        print(type(job_id))
        return jsonify({"error": "Invalid job ID"}), 400

    print("job_id: ", (job_id))
    userid = session['user_id']

    jobs_service = JobsService()
    jobs_service.apply_to_job(userid, (job_id))
    return jsonify({"message": "Job application submitted successfully"})

# Bookmark Job Route:
@job_blueprint.route('/bookmark_job', methods=['GET', 'POST'])
def bookmark_job():
    if 'user_id' not in session:
        print('user not in session!')
        return jsonify({"error": "Unauthorized access"}), 401
    
    job_id = request.json['jobid']
    print("Bookmaked job_id", job_id)
    if type(job_id) is not int:
        print("Invalid job id: ")
        print(type(job_id))
        return jsonify({"error": "Invalid job ID"}), 400
    
    userid = session['user_id']

    jobs_service = JobsService()
    jobs_service.bookmark_job(userid, job_id)
    return jsonify({"message": "Job bookmarked successfully"})

# Get all available jobs Route
@job_blueprint.route('/available_jobs')
def available_jobs():
    # session_type = current_app.config.get('SESSION_TYPE')
    # # print("AVAILABLE JOBS session_type: ", session_type)
    # # print('Available Jobs Session after login:', session, "session user_id:", session['user_id'], "user id in session:", "user_id" in session)
    # # print("Available Jobs: ", session.get('user_id')["email"])
    jobs_service = JobsService()
    jobs = jobs_service.get_available_jobs()
    print(f"Available jobs: {jobs}")
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