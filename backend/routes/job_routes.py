from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
import datetime
from service.seeker_service import SeekerService
from models import Seeker, Job, Company, Application, Technology, JobTechnology
from service.jobs_service import JobsService
from auth.decorators import requires_auth
from flask_cors import CORS
from extensions import db
from flask_caching import Cache
from utils.time import get_relative_time
from flask_caching import Cache
from sqlalchemy import and_, func, or_, desc
from extensions import cache
from utils.technologies import icons
from models import Bookmark;
import json
import os
import config


job_blueprint = Blueprint('job', __name__)
jobs_service = JobsService()
CORS(job_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})

# Get Job Post Page by Job ID:
@job_blueprint.route('/api/job_post/<int:job_id>', methods=['GET'])
def get_job_post_page(job_id):
    job_data = jobs_service.get_job_post_data(job_id)
    if not job_data:
        return jsonify({"error": "Job or company not found"}), 404
    return jsonify(job_data)

@job_blueprint.route('/api/filtered_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def filtered_search_jobs():
    # Get filter criteria and pagination parameters from request
    filter_params = {
        'specialization': request.args.get('specialization'),
        'experience_level': request.args.get('experience_level'),
        'min_experience_years': request.args.get('min_experience_years'),
        'work_location': request.args.get('work_location'),
        'industry': request.args.get('industry'),
        'salary_range': request.args.get('salary_range'),
        'city': request.args.get('city'),
        'tech_stack': request.args.get('tech_stack')
    }
    page = request.args.get('page', default=1, type=int)
    page_size = request.args.get('page_size', default=10, type=int)

    results, total_jobs = jobs_service.filtered_search_jobs(filter_params, page, page_size)

    return jsonify({
        'total': total_jobs,
        'results': results
    })

@job_blueprint.route('/api/instant_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def instant_search_jobs():
    query = request.args.get('query', '')
    page = request.args.get('page', 1, type=int)
    page_size = request.args.get('page_size', 10, type=int)

    results, total_jobs = jobs_service.instant_search_jobs(query, page, page_size)

    return jsonify({
        'total': total_jobs,
        'results': results,
        'page': page,
        'page_size': page_size
    })

@job_blueprint.route('/api/home_page_jobs', methods=['GET'])
def get_home_page_jobs():
    all_jobs = jobs_service.get_home_page_jobs()
    
    return jsonify({
        'jobs': all_jobs,
        'total_jobs': sum(len(jobs) for jobs in all_jobs.values())
    })

@job_blueprint.route('/api/technologies', methods=['GET'])
def get_technologies():
    technology_list = jobs_service.get_technologies()
    return jsonify(technology_list)

@job_blueprint.route('/api/apply_to_job', methods=['POST'])
@requires_auth
def apply_to_job():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    if session['user']['type'] == "recruiter":
        return jsonify({"error": "Unauthorized access: Cannot Apply to Job as a Recruiter"}), 401
    
    job_id = request.json.get('jobid')
    if not isinstance(job_id, int):
        return jsonify({"error": "Invalid job ID"}), 400
    
    seeker_id = session['user']['uid']
    if seeker_id is None:
        return jsonify({"error": "No UserId found"}), 400
    
    try:
        jobs_service.apply_to_job(seeker_id, job_id)
        return jsonify({"message": "Job application submitted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@job_blueprint.route('/api/bookmark_job', methods=['POST'])
@requires_auth
def bookmark_job():
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    if session['user']['type'] == "recruiter":
        return jsonify({"error": "Unauthorized access: Cannot Bookmark Job as a Recruiter"}), 401
    
    job_id = request.json.get('jobid')
    if not isinstance(job_id, int):
        return jsonify({"error": "Invalid job ID"}), 400
    
    seeker_id = session['user']['uid']
    if seeker_id is None:
        return jsonify({"error": "No UserId found"}), 400
    
    try:
        jobs_service.bookmark_job(seeker_id, job_id)
        return jsonify({"message": "Job bookmarked successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

@job_blueprint.route('/api/is_job_applied/<int:job_id>', methods=['GET'])
@requires_auth
def is_job_applied(job_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
        
    user_id = session['user']['uid']
    is_applied = jobs_service.is_job_applied(user_id, job_id)
        
    return jsonify({"is_applied": is_applied})
    
@job_blueprint.route('/api/is_job_saved/<int:job_id>', methods=['GET'])
@requires_auth
def is_job_saved(job_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
        
    user_id = session['user']['uid']
    is_saved = jobs_service.is_job_saved(user_id, job_id)
        
    return jsonify({"is_saved": is_saved})

@job_blueprint.route('/api/unsave_job/<int:job_id>', methods=['DELETE'])
@requires_auth
def unsave_job(job_id):
    if 'user' not in session:
        return jsonify({"error": "Unauthorized access"}), 401
    
    user_id = session['user']['uid']
    try:
        jobs_service.unsave_job(user_id, job_id)
        return jsonify({"message": "Job unsaved successfully"}), 200
    except ValueError as e:
        return jsonify({"error": str(e)}), 404
    
