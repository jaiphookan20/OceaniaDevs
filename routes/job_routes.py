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
@job_blueprint.route('/filter_jobs', methods=['POST', 'GET'])
def filter_jobs():
    filter_data = request.json

    company_id = filter_data.get('company')
    experience_level = filter_data.get('experience_level')
    industry = filter_data.get('industry')
    job_type = filter_data.get('job_type')
    salary_range = filter_data.get('salary_range')
    # salary_type = filter_data.get('salary_type')
    work_location = filter_data.get('work_location')
    specialization = filter_data.get('specialization')
    min_experience_years = filter_data.get('min_experience_years')
    tech_stack = filter_data.get('tech_stack')
    city = filter_data.get('city')
    state = filter_data.get('state')
    country = filter_data.get('country')
    expiry_date = filter_data.get('expiry_date')
    work_rights = filter_data.get('work_rights')
    experience_level = filter_data.get('experience_level')

    jobs_service = JobsService()
    filtered_jobs = jobs_service.filter_jobs(company_id, experience_level, industry, job_type, salary_range,
                                             work_location, min_experience_years, tech_stack, city,
                                             state, country, expiry_date, work_rights, specialization)
    
    # Convert the filtered jobs to a list of dictionaries
    jobs_data = [
        {
            'job_id': job.job_id,
            'title': job.title,
            'company_name': job.company_name,
            'city': job.city,
            'state': job.state,
            'country': job.country,
            'work_location': job.work_location,
            'min_experience_years': job.min_experience_years,
            'specialization': job.specialization,
            'experience_level': job.experience_level
        }
        for job in filtered_jobs
    ]

    # Return the jobs data as a JSON response
    return jsonify(jobs_data)

    # return render_template('filtered_jobs.html', jobs=filtered_jobs)