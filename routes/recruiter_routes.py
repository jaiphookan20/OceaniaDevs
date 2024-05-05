from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.recruiter_service import RecruiterService
from service.jobs_service import JobsService

recruiter_blueprint = Blueprint('recruiter', __name__)

# Add Recruiter Route:
@recruiter_blueprint.route('/add_recruiter', methods=['GET', 'POST'])
def add_recruiter():
    recruiter_service = RecruiterService()
    jobs_service = JobsService()
    if request.method == 'GET':
        # Fetch companies and render the add_recruiter.html template
        companies = jobs_service.get_companies()
        return render_template('add_recruiter.html', companies=companies)
    else:
        # Extract form data and call the add_recruiter method of RecruiterService
        company_id = request.form['company_id']
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        is_direct_recruiter = request.form['is_direct_recruiter'].lower() == 'true'

        recruiter_service.add_recruiter(company_id, first_name, last_name, email,
                                        password, city, state, country, is_direct_recruiter)

        return jsonify({"message": "Recruiter added successfully"})

# Add Company Route:
@recruiter_blueprint.route('/add_company', methods=['GET', 'POST'])
def add_company():
    if request.method == 'GET':
        return render_template('add_company.html')
    else:
        # Extract form data and call the add_company method of CompanyService
        name = request.form['name']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        recruiter_service = RecruiterService()
        recruiter_service.add_company(name, city, state, country)

        return "Company added successfully!"


# Add Job Post Route;
@recruiter_blueprint.route('/add_job', methods=['GET', 'POST'])
def add_job():

    recruiter_service = RecruiterService()
    jobs_service = JobsService()
    
    if request.method == 'GET':
        # Fetch recruiters and companies and render the add_job.html template
        recruiters = jobs_service.get_recruiters()
        companies = jobs_service.get_companies()
        return render_template('add_job.html', recruiters=recruiters, companies=companies)
    else:
        # Extract form data and call the add_job method of JobsService
        recruiter_id = request.form['recruiter_id']
        company_id = request.form['company_id']
        title = request.form['title']
        description = request.form['description']
        specialization = request.form['specialization']
        job_type = request.form['job_type']
        industry = request.form['industry']
        salary_range = request.form['salary_range']
        salary_type = request.form['salary_type']
        work_location = request.form['work_location']
        min_experience_years = request.form['min_experience_years']
        experience_level = request.form['experience_level']
        tech_stack = request.form['tech_stack']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        jobpost_url = request.form['jobpost_url']
        work_rights = request.form.getlist('work_rights')

        recruiter_service.add_job(recruiter_id, company_id, title, description, specialization,
                             job_type, industry, salary_range, salary_type, work_location,
                             min_experience_years, experience_level, tech_stack, city,
                             state, country, jobpost_url, work_rights)

        return jsonify({"message": "Job added successfully"})
    
# HAVE NOT TESTED THIS AS YET
@recruiter_blueprint.route('/update_job/<int:job_id>', methods=['GET', 'POST'])
def update_job(job_id):
    jobs_service = JobsService()
    if request.method == 'GET':
        job = jobs_service.get_job_by_id(job_id)
        if job:
            return render_template('update_job.html', job=job)
        else:
            return "Job not found", 404
    elif request.method == 'POST':
        # Construct a dictionary of updates from the form fields
        updates = {key: request.form[key] for key in request.form}
        jobs_service.update_job(job_id, updates)
        return redirect(url_for('job_bp.available_jobs'))