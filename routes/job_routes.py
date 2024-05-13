from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from service.seeker_service import SeekerService
from models import Seeker
from service.jobs_service import JobsService
from auth.decorators import requires_auth
from flask_cors import CORS

job_blueprint = Blueprint('job', __name__)
cors = CORS(job_blueprint)

# Apply to Job Route:
@job_blueprint.route('/apply_to_job', methods=['GET', 'POST'])
# @requires_auth
def apply_to_job():
    if 'user' not in session:
        print('user not in session!')
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        print('user in session')
        
        job_id = request.json['jobid']
        if type(job_id) is not int:
            print("Invalid job id: ")
            print(type(job_id))
            return jsonify({"error": "Invalid job ID"}), 400
        
        if session['user']['type'] == "recruiter":
            print("Unauthorized access: Cannot Apply to Job as a Recruiter")
            return jsonify({"error": "Unauthorized access"}), 401
        
        else:  
            seeker_id = session['user']['uid'];  
            if seeker_id is None:
                return jsonify({"error": "No UserId found"}), 400
            else:
                userid = seeker_id
                print(f"userid: {userid}")
                print("job_id: ", (job_id))
                jobs_service = JobsService()
                jobs_service.apply_to_job(userid, (job_id))
                return jsonify({"message": "Job application submitted successfully"})

# Bookmark Job Route:
@job_blueprint.route('/bookmark_job', methods=['GET', 'POST'])
# @requires_auth
def bookmark_job():
    if 'user' not in session:
        print('user not in session!')
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        print('user in session')
        
        job_id = request.json['jobid']
        if type(job_id) is not int:
            print("Invalid job id: ")
            print(type(job_id))
            return jsonify({"error": "Invalid job ID"}), 400
        
        if session['user']['type'] == "recruiter":
            print("Unauthorized access: Cannot Bookmark Job as a Recruiter")
            return jsonify({"error": "Unauthorized access"}), 401
        
        else:  
            seeker_id = session['user']['uid'];  
            if seeker_id is None:
                return jsonify({"error": "No UserId found"}), 400
            else:
                userid = seeker_id
                print(f"userid: {userid}")
                print("job_id: ", (job_id))
                jobs_service = JobsService()
                jobs_service.bookmark_job(userid, (job_id))
                return jsonify({"message": "Job Bookmaked successfully"})
            
# Get all available jobs Route
@job_blueprint.route('/available_jobs')
def available_jobs():
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