from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
import datetime
from service.seeker_service import SeekerService
from models import Seeker, Job, Company
from service.jobs_service import JobsService
from auth.decorators import requires_auth
from flask_cors import CORS
from extensions import db
from flask_caching import Cache
from utils.time import get_relative_time
from flask_caching import Cache
from sqlalchemy import and_, func, or_
from extensions import cache
import os


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


@job_blueprint.route('/api/job_post/<int:job_id>', methods=['GET'])
def get_job_post_page(job_id):
    jobs_service = JobsService()
    job = jobs_service.get_job_by_id(job_id)
    company = jobs_service.get_company_by_id(job.company_id)
    
    if not job or not company:
        return jsonify({"error": "Job or company not found"}), 404

    company_name_lower = company.name.lower() if company.name else ''
    company_logo = company.logo_url if company.logo_url else company_logos.get(company_name_lower, '')

    # Ensure the logo path is fully qualified
    if company_logo and not company_logo.startswith('http'):
        company_logo = f"http://127.0.0.1:4040/uploads/{os.path.basename(company_logo)}"

    job_data = {
        'job_id': job.job_id,
        'title': job.title,
        'company': company.name,
        'company_logo': company_logo,
        'industry': job.industry,
        'salary_range': job.salary_range,
        'country': job.country,
        'specialization': job.specialization,
        'salary_type': job.salary_type,
        'work_location': job.work_location,
        'location': f"{job.city}, {job.state}",
        'min_experience_years': job.min_experience_years,
        'experience_level': job.experience_level,
        'city': job.city,
        'description': job.description,
        'state': job.state,
        'work_rights': job.work_rights,
        'description': job.description,
        'tech_stack': job.tech_stack
    }

    return jsonify(job_data)


@job_blueprint.route('/api/alljobs', methods=['GET'])
def get_all_jobs():
    """
    Fetch all jobs with pagination.
    
    Query Parameters:
        page (int): The page number to fetch.
        page_size (int): The number of jobs per page.
    
    Returns:
        json: A JSON response containing job data, page info, and total job count.
    """
    # Get the page number from the request
    page = request.args.get('page', 1, type=int)  
    # Get the page size from the request
    page_size = request.args.get('page_size', 25, type=int)   
    
    jobs_service = JobsService()  # Initialize the JobsService

    jobs, total_jobs = jobs_service.get_available_jobs_with_pagination(page, page_size)  # Fetch paginated jobs

    # Format the job data for the response
    jobs_data = []
    for job in jobs:
        company_logo = job.Company.logo_url if job.Company.logo_url else company_logos.get(job.Company.name.lower(), '')
        
        # Ensure the logo path is fully qualified
        if job.Company.logo_url: 
            if not company_logo.startswith('http'):
                company_logo = f"http://127.0.0.1:4040/uploads/{os.path.basename(company_logo)}"
        
        job_data = {
            'title': job.Job.title,
            'company': job.Company.name,  # Accessing company name from the Company table
            'location': f"{job.Job.city}, {job.Job.state}",
            'city': job.Job.city,
            'experience_level': job.Job.experience_level,
            'job_id': job.Job.job_id,
            'salary_range': job.Job.salary_range,
            'logo': company_logo,
            'specialization': job.Job.specialization,
            'created_at': get_relative_time(job.Job.created_at.strftime('%Y-%m-%d')),
            'tech_stack': job.Job.tech_stack
        }
        jobs_data.append(job_data)
    
    # Return the job data, page info, and total job count
    return jsonify({
        'jobs': jobs_data,
        'page': page,
        'page_size': page_size,
        'total_jobs': total_jobs
    })

# Apply to Job Route:
@job_blueprint.route('/api/apply_to_job', methods=['GET', 'POST'])
@requires_auth
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
@job_blueprint.route('/api/bookmark_job', methods=['GET', 'POST'])
@requires_auth
def bookmark_job():
    if 'user' not in session:
        print('Cannot Bookmark. User not in session!')
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
@job_blueprint.route('/api/available_jobs')
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
    
# Instant search jobs route
@job_blueprint.route('/api/instant_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def instant_search_jobs():
    """
    Performs an instant search for jobs based on the provided query.
    The results are cached for 60 seconds.
    """
    query = request.args.get('query', '')
    print(f"Received query: {query}")  # Debugging log

    if query:
        # Construct the search query
        search_query = func.plainto_tsquery('english', query)

        try:
            # Execute the query and fetch all results
            jobs_query = Job.query.filter(
                or_(
                    # Search for jobs where the search vector matches the search query
                    Job.search_vector.op('@@')(search_query),
                    # Search for jobs where the company name contains the search query (case-insensitive)
                    Company.name.ilike(f'%{query}%')
                )).join(
                # Join the Job and Company tables based on the company_id foreign key
                Company, Job.company_id == Company.company_id).add_columns(
                # Select the following columns from the Job and Company tables
                Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country,
                Job.salary_range, Job.created_at, Job.experience_level, Company.name.label('company_name')
            )
            
            jobs = jobs_query.all()
            print(f"Jobs found: {len(jobs)}")  # Debugging log
            
            # Format the results
            results = [{
                'job_id': job.job_id,
                'title': job.title,
                'company': job.company_name,
                'city': job.city,
                'specialization': job.specialization,
                'country': job.country,
                'salary_range': job.salary_range,
                'created_at': job.created_at.strftime('%Y-%m-%d'),
                'experience_level': job.experience_level,
                'logo': company_logos.get(job.company_name.lower(), ''),
            } for job in jobs]

            return jsonify({
                'total': len(results),
                'results': results
            })

        except Exception as e:
            print(f"Error during job search: {e}")  # Debugging log
            return jsonify({
                'total': 0,
                'results': [],
                'error': str(e)
            })

    else:
        return jsonify({
            'total': 0,
            'results': []
        })

# NOTE: Need to inspect this route again - IS NOT WORKING CORRECTLY. DOES NOT give the right answers as before for some queries? for eg: choosing backend for specialization returning only 2 jobs, which is incorrect
# Filtered search jobs route
@job_blueprint.route('/api/filtered_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def filtered_search_jobs():
    """
    Performs a filtered search for jobs based on various criteria.
    The results are cached for 60 seconds.
    """
    # Get the filter criteria from the request arguments
    specialization = request.args.get('specialization')
    experience_level = request.args.get('experience_level')
    min_experience_years = request.args.get('min_experience_years')
    work_location = request.args.get('work_location')
    industry = request.args.get('industry')
    salary_range = request.args.get('salary_range')
    city = request.args.get('city')
    tech_stack = request.args.get('tech_stack')

    # Initialize the jobs query
    jobs_query = Job.query

    # Apply filters based on the provided criteria
    if specialization:
        jobs_query = jobs_query.filter(Job.specialization == specialization)
    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)
    if min_experience_years:
        jobs_query = jobs_query.filter(Job.min_experience_years >= min_experience_years)
    if work_location:
        jobs_query = jobs_query.filter(or_(Job.city == work_location, Job.state == work_location, Job.country == work_location))
    if industry:
        jobs_query = jobs_query.filter(Job.industry == industry)
    if salary_range:
        jobs_query = jobs_query.filter(Job.salary_range == salary_range)
    if tech_stack:
        jobs_query = jobs_query.filter(Job.tech_stack.any(tech_stack))

    # Execute the query and format the results
    jobs = jobs_query.join(Company, Job.company_id == Company.company_id).add_columns(
        Job.job_id, Job.title, Job.description, Job.specialization, Job.salary_range, Job.city, Job.state, Job.country, Job.salary_range, 
        Job.created_at, Job.experience_level, Company.name.label('company_name'), Company.logo_url.label('logo')).all()

    results = [{
        'job_id': job.job_id,
        'title': job.title,
        'company': job.company_name,
        'city': job.city,
        'location': f"{job.city}, {job.state}",
        'country': job.country,
        'salary_range': job.salary_range,
        'created_at': job.created_at.strftime('%Y-%m-%d'),
        'experience_level': job.experience_level,
        'specialization': job.specialization,
        'logo': company_logos.get(job.company_name.lower(), ''),
    } for job in jobs]

    return jsonify({
        'total': len(results),
        'results': results
    })