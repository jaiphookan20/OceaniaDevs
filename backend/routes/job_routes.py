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
from utils.technologies import icons
from models import Bookmark;
import json
import os
import config


job_blueprint = Blueprint('job', __name__)
CORS(job_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})

# Get Job Post Page by Job ID:
@job_blueprint.route('/api/job_post/<int:job_id>', methods=['GET'])
def get_job_post_page(job_id):
    jobs_service = JobsService()
    job = jobs_service.get_job_by_id(job_id)
    company = jobs_service.get_company_by_id(job.company_id)
    
    if not job or not company:
        return jsonify({"error": "Job or company not found"}), 404
    
    # Helper function to parse text to list
    def parse_text_to_list(text):
        if not text:
            return []
        try:
            # Try to parse as JSON first
            return json.loads(text)
        except json.JSONDecodeError:
            # If not JSON, split by newlines and remove empty strings
            return [item.strip() for item in text.split('\n') if item.strip()]

    job_data = {
        'job_id': job.job_id,
        'title': job.title,
        'company': company.name,
        'overview': job.overview,
        'responsibilities': parse_text_to_list(job.responsibilities),
        'requirements': parse_text_to_list(job.requirements),
        'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
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
        'tech_stack': job.tech_stack,
        'daily_range': job.daily_range,
        'hourly_range': job.hourly_range,
        'contract_duration':job.contract_duration,
        'job_arrangement': job.job_arrangement,
        'jobpost_url': job.jobpost_url,
    }

    return jsonify(job_data)

# Get All Jobs ie Populate Job Feed:
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
                
        job_data = {
            'title': job.Job.title,
            'company': job.Company.name,  # Accessing company name from the Company table
            'location': f"{job.Job.city}, {job.Job.state}",
            'city': job.Job.city,
            'experience_level': job.Job.experience_level,
            'job_id': job.Job.job_id,
            'salary_range': job.Job.salary_range,
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.Company.logo_url)}",
            'specialization': job.Job.specialization,
            'min_experience_years': job.Job.min_experience_years,
            'created_at': get_relative_time(job.Job.created_at.strftime('%Y-%m-%d')),
            'tech_stack': job.Job.tech_stack,
            'jobpost_url': job.Job.jobpost_url        
        }
        # current_app.logger.info(f"Job Data: {job_data}")
        jobs_data.append(job_data)
    
    # Return the job data, page info, and total job count
    return jsonify({
        'jobs': jobs_data,
        'page': page,
        'page_size': page_size,
        'total_jobs': total_jobs
    })

# Apply to Job Post:
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

# Bookmark a Job Post:
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
                
# Filtered Search Jobs
# @job_blueprint.route('/api/filtered_search_jobs', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
# def filtered_search_jobs():
#     """
#     Performs a filtered search for jobs based on various criteria.
#     The results are cached for 60 seconds.
#     """
#     # Get the filter criteria from the request arguments
#     specialization = request.args.get('specialization')
#     experience_level = request.args.get('experience_level')
#     min_experience_years = request.args.get('min_experience_years')
#     work_location = request.args.get('work_location')
#     industry = request.args.get('industry')
#     salary_range = request.args.get('salary_range')
#     city = request.args.get('city')
#     # tech_stack = request.args.get('tech_stack')
#     tech_stack = request.args.getlist('tech_stack')

#     # Initialize the jobs query
#     jobs_query = Job.query

#     # Apply filters based on the provided criteria
#     if specialization:
#         jobs_query = jobs_query.filter(Job.specialization == specialization)
#     if experience_level:
#         jobs_query = jobs_query.filter(Job.experience_level == experience_level)
#     if min_experience_years:
#         jobs_query = jobs_query.filter(Job.min_experience_years >= min_experience_years)
#     if work_location:
#         jobs_query = jobs_query.filter(or_(Job.city == work_location, Job.state == work_location, Job.country == work_location))
#     if industry:
#         jobs_query = jobs_query.filter(Job.industry == industry)
#     if salary_range:
#         jobs_query = jobs_query.filter(Job.salary_range == salary_range)
#     if tech_stack:
#         jobs_query = jobs_query.filter(Job.tech_stack.any(tech_stack))
    
#     # Execute the query and format the results
#     jobs = jobs_query.join(Company, Job.company_id == Company.company_id).add_columns(
#         Job.job_id, Job.title, Job.description, Job.specialization, Job.salary_range, Job.city, Job.state, Job.country, Job.salary_range, 
#         Job.created_at, Job.experience_level, Company.name.label('company_name'), Company.logo_url.label('logo_url')).all()
    
#     results = [{
#     'job_id': job.job_id,
#     'title': job.title,
#     'company': job.company_name,
#     'city': job.city,
#     'location': f"{job.city}, {job.state}",
#     'country': job.country,
#     'salary_range': job.salary_range,
#     'created_at': job.created_at.strftime('%Y-%m-%d'),
#     'experience_level': job.experience_level,
#     'specialization': job.specialization,
#     'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo_url)}",
# } for job in jobs]

#     return jsonify({
#         'total': len(results),
#         'results': results
#     })

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
    tech_stack = request.args.get('tech_stack')  # Changed to get a single value

    # Initialize the jobs query
    jobs_query = Job.query.join(Company, Job.company_id == Company.company_id)

    # Apply filters based on the provided criteria
    if specialization:
        jobs_query = jobs_query.filter(Job.specialization == specialization)
    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)
    if min_experience_years:
        jobs_query = jobs_query.filter(Job.min_experience_years >= int(min_experience_years))
    if work_location:
        jobs_query = jobs_query.filter(or_(Job.city.ilike(f"%{work_location}%"),
                                           Job.state.ilike(f"%{work_location}%"),
                                           Job.country.ilike(f"%{work_location}%")))
    if industry:
        jobs_query = jobs_query.filter(Job.industry == industry)
    if salary_range:
        jobs_query = jobs_query.filter(Job.salary_range == salary_range)
    if city:
        jobs_query = jobs_query.filter(Job.city.ilike(f"%{city}%"))
    if tech_stack:
        jobs_query = jobs_query.filter(Job.tech_stack.cast(db.String).ilike(f"%{tech_stack}%"))

    # Execute the query and format the results
    jobs = jobs_query.add_columns(
        Job.job_id, Job.title, Job.description, Job.specialization, Job.salary_range,
        Job.city, Job.state, Job.country, Job.created_at, Job.experience_level,
        Job.tech_stack, Company.name.label('company_name'), Company.logo_url.label('logo_url'), Job.min_experience_years
    ).all()

    results = [{
        'job_id': job.job_id,
        'title': job.title,
        'company': job.company_name,
        'city': job.city,
        'location': f"{job.city}, {job.state}",
        'country': job.country,
        'salary_range': job.salary_range,
        'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
        'experience_level': job.experience_level,
        'specialization': job.specialization,
        'min_experience_years': job.min_experience_years,
        'tech_stack': job.tech_stack,
        'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo_url)}",
    } for job in jobs]

    return jsonify({
        'total': len(results),
        'results': results
    })

# @job_blueprint.route('/api/instant_search_jobs', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
# def instant_search_jobs():
#     query = request.args.get('query', '')
#     current_app.logger.info(f"Received query: {query}")

#     if query:
#         search_query = func.plainto_tsquery('english', query)
#         jobs_query = Job.query.filter(
#             or_(
#                 Job.search_vector.op('@@')(search_query),
#                 Company.name.ilike(f'%{query}%')
#             )
#         ).join(Company, Job.company_id == Company.company_id).add_columns(
#             Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country, Job.salary_range, Job.created_at, Job.experience_level, Company.name.label('company_name'), Company.logo_url.label('logo_url')
#         )
        
#         jobs = jobs_query.all()
#         results = [{
#             'job_id': job.job_id,
#             'title': job.title,
#             'company': job.company_name,
#             'city': job.city,
#             'specialization': job.specialization,
#             'country': job.country,
#             'salary_range': job.salary_range,
#             'created_at': job.created_at.strftime('%Y-%m-%d'),
#             'experience_level': job.experience_level,
#             'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo_url)}",
#         } for job in jobs]
        
#         current_app.logger.info(f"Total Results: {len(results)}")
#         current_app.logger.info(f"Results: {results}")
        
#         return jsonify({
#             'total': len(results),
#             'results': results
#         })
#     else:
#         return jsonify({
#             'total': 0,
#             'results': []
#         })


# @job_blueprint.route('/api/instant_search_jobs', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
# def instant_search_jobs():
#     query = request.args.get('query', '')
#     current_app.logger.info(f"Received query: {query}")

#     if query:
#         search_terms = query.split()
#         search_query = ' & '.join(search_terms)
#         tsquery = func.to_tsquery('english', search_query)
        
#         jobs_query = Job.query.join(Company).filter(
#             or_(
#                 Job.search_vector.op('@@')(tsquery),
#                 Company.name.ilike(f'%{query}%'),
#                 Job.title.ilike(f'%{query}%'),
#                 Job.description.ilike(f'%{query}%'),
#                 Job.specialization.ilike(f'%{query}%'),
#                 Job.city.ilike(f'%{query}%'),
#                 Job.state.ilike(f'%{query}%'),
#                 Job.country.ilike(f'%{query}%'),
#                 Job.tech_stack.any(lambda x: x.ilike(f'%{query}%'))
#             )
#         ).add_columns(
#             Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country,
#             Job.salary_range, Job.created_at, Job.experience_level, Job.tech_stack,
#             Company.name.label('company_name'), Company.logo_url.label('logo_url')
#         ).order_by(func.ts_rank(Job.search_vector, tsquery).desc())

#         # Debug: Print the SQL query
#         current_app.logger.info(f"SQL Query: {jobs_query}")

#         jobs = jobs_query.all()
        
#         # Debug: Print raw job data
#         current_app.logger.info(f"Raw job data: {jobs}")

#         results = [{
#             'job_id': job.job_id,
#             'title': job.title,
#             'company': job.company_name,
#             'city': job.city,
#             'specialization': job.specialization,
#             'country': job.country,
#             'salary_range': job.salary_range,
#             'created_at': job.created_at.strftime('%Y-%m-%d'),
#             'experience_level': job.experience_level,
#             'tech_stack': job.tech_stack,
#             'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo_url)}",
#         } for job in jobs]
        
#         current_app.logger.info(f"Total Results: {len(results)}")
#         current_app.logger.info(f"Results: {results}")
        
#         return jsonify({
#             'total': len(results),
#             'results': results
#         })
#     else:
#         return jsonify({
#             'total': 0,
#             'results': []
#         })


@job_blueprint.route('/api/instant_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def instant_search_jobs():
    query = request.args.get('query', '')
    current_app.logger.info(f"Received query: {query}")

    if query:
        search_terms = query.split()
        search_query = ' | '.join(search_terms)  # Use OR for more flexible matching
        tsquery = func.to_tsquery('english', search_query)
        
        jobs_query = Job.query.join(Company).filter(
            or_(
                Job.search_vector.op('@@')(tsquery),
                Company.name.ilike(f'%{query}%')  # Keep this for company name search
            )
        ).add_columns(
            Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country,
            Job.salary_range, Job.created_at, Job.experience_level, Job.tech_stack,
            Company.name.label('company_name'), Company.logo_url.label('logo_url'), Job.min_experience_years,
        ).order_by(func.ts_rank(Job.search_vector, tsquery).desc())

        # Debug: Print the SQL query
        current_app.logger.info(f"SQL Query: {jobs_query}")

        jobs = jobs_query.all()
        
        # Debug: Print raw job data
        current_app.logger.info(f"Raw job data: {jobs}")

        results = [{
            'job_id': job.job_id,
            'title': job.title,
            'company': job.company_name,
            'city': job.city,
            'specialization': job.specialization,
            'country': job.country,
            'salary_range': job.salary_range,
            'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
            'experience_level': job.experience_level,
            'min_experience_years': job.min_experience_years,
            'tech_stack': job.tech_stack,
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo_url)}",
        } for job in jobs]
        
        current_app.logger.info(f"Total Results: {len(results)}")
        current_app.logger.info(f"Results: {results}")
        
        return jsonify({
            'total': len(results),
            'results': results
        })
    else:
        return jsonify({
            'total': 0,
            'results': []
        })

    
@job_blueprint.route('/api/is_job_saved/<int:job_id>', methods=['GET'])
@requires_auth
def is_job_saved(job_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
        
    user_id = session['user']['uid']
    bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
        
    return jsonify({"is_saved": bookmark is not None})


@job_blueprint.route('/api/unsave_job/<int:job_id>', methods=['DELETE'])
@requires_auth
def unsave_job(job_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    user_id = session['user']['uid']
    bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
    
    if bookmark:
        db.session.delete(bookmark)
        db.session.commit()
        return jsonify({"message": "Job unsaved successfully"}), 200
    else:
        return jsonify({"error": "Job was not saved"}), 404