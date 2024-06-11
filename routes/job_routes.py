from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
import datetime
from service.seeker_service import SeekerService
from models import Seeker, Job, Company
from service.jobs_service import JobsService
from auth.decorators import requires_auth
from flask_cors import CORS
from extensions import db
from flask_caching import Cache


job_blueprint = Blueprint('job', __name__)
CORS(job_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})

icons = {
    'aws': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/amazonwebservices/amazonwebservices-original-wordmark.svg" />',
    "docker": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/docker/docker-original.svg" />',
    "gcp": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/googlecloud/googlecloud-original.svg" />',
    "kubernetes": '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/kubernetes/kubernetes-original-wordmark.svg" />',
    'angular': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/angularjs/angularjs-original.svg" />',
    'grafana': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/grafana/grafana-original.svg" />',
    'terraform': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/terraform/terraform-original.svg" />',
    'prometheus': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/prometheus/prometheus-original.svg" />',
    'azure': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/azure/azure-original.svg" />',
    'java': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/java/java-original.svg" />',
    'linux': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/linux/linux-original.svg" />',
    'nextjs': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nextjs/nextjs-original-wordmark.svg" />',
    'nestjs': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nestjs/nestjs-original-wordmark.svg" />',
    'nginx': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nginx/nginx-original.svg" />',
    'postgresql': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/postgresql/postgresql-original.svg" />',
    'kafka': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/apachekafka/apachekafka-original-wordmark.svg" />',
    'spring': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/spring/spring-original.svg" />',
    'node.js':'<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg" />',
    'typescript':'<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/typescript/typescript-original.svg" />',
    'javascript': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/javascript/javascript-original.svg" />', 
    'nodejs': '<img src="https://cdn.jsdelivr.net/gh/devicons/devicon@latest/icons/nodejs/nodejs-original-wordmark.svg" />'                   
}

company_logos = {
    'airwallex': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzDHDDJYBvqPYjfZnQXrnhMFJiRBeNurLCEA&s',
    'oceaniadevs': 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcTzDHDDJYBvqPYjfZnQXrnhMFJiRBeNurLCEA&s',
    'xero': 'https://upload.wikimedia.org/wikipedia/en/archive/9/9f/20171204173437%21Xero_software_logo.svg',
    'canva': 'https://builtin.com/sites/www.builtin.com/files/2021-11/CIRCLE%20LOGO%20-%20GRADIENT%20-%20RGB_0.png',
    'atlassian': 'https://cdn.prod.website-files.com/6350c9fce59bc08494e7e9e5/6542fe0e8e219ee96075cb7a_638439dd30aa4b831f8f5873_Atlassian-Logo.png',
    'cultureamp': 'https://seeklogo.com/images/C/culture-amp-logo-F3EE0956BD-seeklogo.com.png'
}

@job_blueprint.route('/job_post/<int:job_id>')
def get_job_post_page(job_id):
    jobs_service = JobsService()
    job = jobs_service.get_job_by_id(job_id)
    company = jobs_service.get_company_by_id(job.company_id)
    
    company_name_lower = company.name.lower() if company.name else ''
    company_logo = company_logos.get(company_name_lower, '')
    
    return render_template('job_post.html', job=job, company=company, icons=icons, company_logo=company_logo)

# New API endpoint to fetch jobs data
@job_blueprint.route('/alljobs')
def get_jobs():
    jobs_service = JobsService()
    jobs = jobs_service.get_available_jobs()
    return jsonify([{
        'title': job.title,
        'company': job.company_name,
        'location': f"{job.city}, {job.state}",
        'city': job.city,
        'experience_level': job.experience_level,
        'job_id': job.job_id,
        'salary_range': job.salary_range,
        # 'date': job.created_at.strftime('%Y-%m-%d'),
        'logo': company_logos.get(job.company_name.lower(), ''),
        'specialization': job.specialization,
        'tech_stack': job.tech_stack
        # 'new': job.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
    } for job in jobs])

# Apply to Job Route:
@job_blueprint.route('/apply_to_job', methods=['GET', 'POST'])
# @requires_auth
def apply_to_job():
    if 'user' not in session:
        print('user not in session!')
        return jsonify({"message": "Unauthorized access"}), 401
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
@requires_auth
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