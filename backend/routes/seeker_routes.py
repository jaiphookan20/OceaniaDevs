from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.seeker_service import SeekerService
from service.jobs_service import JobsService
from models import Seeker, Job
from flask_cors import CORS
from utils.time import get_relative_time
import os
import config
from datetime import datetime

# Create a Blueprint for seeker-related routes
seeker_blueprint = Blueprint('seeker', __name__)
CORS(seeker_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost:3000'}})

# Get Bookmarked Jobs Route
# @seeker_blueprint.route('/api/bookmarked_jobs')
# def get_all_bookmarked_jobs_by_seeker():
#     if session['user']['type'] != "seeker":
#         return jsonify({"error": "Unauthorized access"}), 401
#     else:
#         seeker_id = session['user']['uid']
#         print(f"seeker_id: {seeker_id}")
#         seeker_service = SeekerService()
#         jobs_service = JobsService()
#         bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)

#         for bookmarked_job in bookmarked_jobs:
#             company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
#             job = jobs_service.get_job_by_id(bookmarked_job.jobid)
#             bookmarked_job.company_name = company.name if company else "N/A"
#             bookmarked_job.title = job.title if job else "N/A"
#             bookmarked_job.city = job.city if job else "N/A"
#             bookmarked_job.state = job.state if job else "N/A"
#             bookmarked_job.country = job.country if job else "N/A"
#             bookmarked_job.salary_range = job.salary_range if job else "N/A"
#             bookmarked_job.specialization = job.specialization if job else "N/A"
#             bookmarked_job.experience_level = job.experience_level if job else "N/A"
#             bookmarked_job.created_at = job.created_at if job else "N/A"
#             bookmarked_job.min_experience_years = job.min_experience_years if job else "N/A"

#             bookmarked_job.logo = company.logo_url;            

#         return jsonify(bookmarked_jobs=[{
#             'job_id': job.jobid,
#             'title': job.title,
#             'company': job.company_name,
#             'city': job.city,
#             'state': job.state,
#             'country': job.country,
#             'experience_level': job.experience_level,
#             'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo)}",
#             'created_at': job.created_at.strftime('%Y-%m-%d'),
#             'specialization': job.specialization,
#             'salary_range': job.salary_range,
#             'min_experience_years': job.min_experience_years,
#         } for job in bookmarked_jobs])

@seeker_blueprint.route('/api/bookmarked_jobs')
def get_all_bookmarked_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        print(f"seeker_id: {seeker_id}")
        
        seeker_service = SeekerService()
        jobs_service = JobsService()
        # bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id)
        bookmarked_jobs = seeker_service.get_all_bookmarked_jobs_by_seeker(seeker_id, page, page_size)

        for bookmarked_job in bookmarked_jobs:
            company = jobs_service.get_company_by_jobid(bookmarked_job.jobid)
            job = jobs_service.get_job_by_id(bookmarked_job.jobid)
            bookmarked_job.company_name = company.name if company else "N/A"
            bookmarked_job.company_id = company.company_id if company else "N/A"
            bookmarked_job.title = job.title if job else "N/A"
            bookmarked_job.city = job.city if job else "N/A"
            bookmarked_job.state = job.state if job else "N/A"
            bookmarked_job.country = job.country if job else "N/A"
            bookmarked_job.salary_range = job.salary_range if job else "N/A"
            bookmarked_job.specialization = job.specialization if job else "N/A"
            bookmarked_job.experience_level = job.experience_level if job else "N/A"
            bookmarked_job.created_at = job.created_at if job else "N/A"
            bookmarked_job.min_experience_years = job.min_experience_years if job else "N/A"

            bookmarked_job.logo = company.logo_url;            

        return jsonify(bookmarked_jobs=[{
            'job_id': job.jobid,
            'title': job.title,
            'company': job.company_name,
            'city': job.city,
            'state': job.state,
            'country': job.country,
            'experience_level': job.experience_level,
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.logo)}",
            'created_at': job.created_at.strftime('%Y-%m-%d'),
            'specialization': job.specialization,
            'salary_range': job.salary_range,
            'min_experience_years': job.min_experience_years,
            'company_id': job.company_id,
        } for job in bookmarked_jobs])

@seeker_blueprint.route('/api/applied_jobs')
def get_all_applied_jobs_by_seeker():
    if session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        seeker_id = session['user']['uid']
        page = request.args.get('page', 1, type=int)
        page_size = request.args.get('page_size', 10, type=int)
        
        seeker_service = SeekerService()
        jobs_service = JobsService()
        applied_jobs = seeker_service.get_all_applied_jobs_by_seeker(seeker_id, page, page_size)

        applied_jobs_data = []
        for applied_job in applied_jobs:
            company = jobs_service.get_company_by_jobid(applied_job.jobid)
            job = jobs_service.get_job_by_id(applied_job.jobid)
            
            applied_jobs_data.append({
                'job_id': applied_job.jobid,
                'title': job.title if job else "N/A",
                'company': company.name if company else "N/A",
                'city': job.city if job else "N/A",
                'state': job.state if job else "N/A",
                'country': job.country if job else "N/A",
                'experience_level': job.experience_level if job else "N/A",
                'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}" if company and company.logo_url else None,
                'created_at': job.created_at.strftime('%Y-%m-%d') if job and job.created_at else "N/A",
                'specialization': job.specialization if job else "N/A",
                'salary_range': job.salary_range if job else "N/A",
                'applied_at': applied_job.datetimestamp.strftime('%Y-%m-%d'),
                'min_experience_years': job.min_experience_years if job else "N/A",
                'status': applied_job.status if hasattr(applied_job, 'status') else 'Applied'
            })

        return jsonify(applied_jobs=applied_jobs_data)
    
@seeker_blueprint.route('/api/remove_application/<int:job_id>', methods=['DELETE'])
def remove_application(job_id):
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    seeker_id = session['user']['uid']
    seeker_service = SeekerService()
    success = seeker_service.remove_application(seeker_id, job_id)
    
    if success:
        return jsonify({"message": "Application removed successfully"}), 200
    else:
        return jsonify({"error": "Failed to remove application"}), 500


@seeker_blueprint.route('/api/user_applications')
def get_user_applications():
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    seeker_id = session['user']['uid']
    seeker_service = SeekerService()
    jobs_service = JobsService()
    applications = seeker_service.get_user_applications(seeker_id)

    application_data = []
    for app in applications:
        job = jobs_service.get_job_by_id(app.jobid)
        company = jobs_service.get_company_by_jobid(app.jobid)
        
        application_data.append({
            'id': app.applicationid,
            'company': company.name if company else "N/A",
            'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}" if company and company.logo_url else None,
            'position': job.title if job else "N/A",
            'appliedDate': app.datetimestamp.strftime('%Y-%m-%d'),
            'status': app.status if hasattr(app, 'status') else 'Applied',
            'jobId': app.jobid
        })

    return jsonify(applications=application_data)


@seeker_blueprint.route('/api/update_application_status/<int:application_id>', methods=['PUT'])
def update_application_status(application_id):
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    data = request.json
    new_status = data.get('status')
    
    if not new_status:
        return jsonify({"error": "No status provided"}), 400
    
    seeker_service = SeekerService()
    success = seeker_service.update_application_status(application_id, new_status)
    
    if success:
        return jsonify({"message": "Application status updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update application status"}), 500
    

@seeker_blueprint.route('/api/remove_bookmark', methods=['POST'])
def remove_bookmark():
    if 'user' not in session or session['user']['type'] != "seeker":
        return jsonify({"error": "Unauthorized access"}), 401
    
    data = request.json
    job_id = data.get('jobid')
    seeker_id = session['user']['uid']
    
    if not job_id:
        return jsonify({"error": "No job ID provided"}), 400
    
    seeker_service = SeekerService()
    success = seeker_service.remove_bookmark(seeker_id, job_id)
    
    if success:
        return jsonify({"message": "Job removed from bookmarks successfully"}), 200
    else:
        return jsonify({"error": "Failed to remove job from bookmarks"}), 500
    

@seeker_blueprint.route('/api/seeker_info', methods=['GET'])
def get_seeker_info():
    if 'user' not in session or session['user']['type'] != 'seeker':
        return jsonify({"error": "Unauthorized"}), 401

    seeker_service = SeekerService()
    seeker_id = session['user']['uid']
    seeker = seeker_service.get_seeker_by_id(seeker_id)

    if not seeker:
        return jsonify({"error": "Seeker not found"}), 404

    seeker_info = {
        "firstName": seeker.first_name,
        "lastName": seeker.last_name,
        "email": seeker.email,
        "city": seeker.city,
        "state": seeker.state,
        "country": seeker.country
    }

    return jsonify(seeker_info)

# Update Job Seeker Route
@seeker_blueprint.route('/api/update_seeker', methods=['POST'])
def update_seeker():
    if 'user' not in session or session['user']['type'] != 'seeker':
        return jsonify({"error": "Unauthorized access"}), 401

    seeker_service = SeekerService()
    seeker_id = session['user']['uid']
    data = request.json

    result = seeker_service.update_seeker(seeker_id, data)
    if result:
        return jsonify({"message": "Seeker info updated successfully"}), 200
    else:
        return jsonify({"error": "Failed to update seeker info"}), 400
