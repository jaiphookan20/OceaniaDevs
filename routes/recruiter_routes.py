from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify
from service.recruiter_service import RecruiterService
from service.jobs_service import JobsService
from models import Recruiter, Company, Job
from extensions import db

# Create a Blueprint for recruiter-related routes
recruiter_blueprint = Blueprint('recruiter', __name__)

# Add Recruiter Route
@recruiter_blueprint.route('/add_recruiter', methods=['GET', 'POST'])
def add_recruiter():
    """
    Route for adding a new recruiter.
    
    GET: Renders the 'add_recruiter.html' template with a list of companies.
    POST: Extracts form data and calls the 'add_recruiter' method of the RecruiterService.
    
    Returns:
        - For GET: Rendered 'add_recruiter.html' template.
        - For POST: JSON response with a success message.
        - 401 Unauthorized error if the user is not a recruiter or not logged in.
    """
    if 'user' not in session:
        print('user not in session!')
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        print('user in session')
    
        if session.get('user').get('type') != 'recruiter':
            print('user not in session!')
            return jsonify({"error": "Unauthorized access. Only Recruiters can access this resource"}), 401

        else:
            recruiter_service = RecruiterService()
            jobs_service = JobsService()
            if request.method == 'GET':
                # Fetch companies and render the add_recruiter.html template
                companies = jobs_service.get_companies()
                company = recruiter_service.get_company_by_recruiter_id()
                print(f"company: {company}")
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

                recruiter_service.add_recruiter(company_id, first_name, last_name, email,password, city, state, country, is_direct_recruiter)
                return jsonify({"message": "Recruiter added successfully"})
    
# Add Company Route
@recruiter_blueprint.route('/add_company', methods=['GET', 'POST'])
def add_company():
    """
    Route for adding a new company.
    
    GET: Renders the 'add_company.html' template.
    POST: Extracts form data and calls the 'add_company' method of the RecruiterService.
    
    Returns:
        - For GET: Rendered 'add_company.html' template.
        - For POST: Success message.
    """
    if request.method == 'GET':
        return render_template('add_company.html')
    else:
        # Extract form data and call the add_company method of CompanyService
        name = request.form['name']
        website_url = request.form['website_url']

        recruiter_service = RecruiterService()
        recruiter_service.add_company(name, website_url)

        return "Company added successfully!"

# Add Job Post Route
@recruiter_blueprint.route('/add_job', methods=['GET', 'POST'])
def add_job():
    """
    Route for adding a new job post.
    
    GET: Renders the 'add_job.html' template with a list of recruiters and companies.
    POST: Extracts form data and calls the 'add_job' method of the RecruiterService.
    
    Returns:
        - For GET: Rendered 'add_job.html' template.
        - For POST: JSON response with a success message.
    """
    recruiter_service = RecruiterService()
    jobs_service = JobsService()
    
    if request.method == 'GET':
        # Fetch recruiters and companies and render the add_job.html template
        recruiters = jobs_service.get_recruiters()
        companies = jobs_service.get_companies()
        return render_template('add_job.html', recruiters=recruiters, companies=companies)
    else:
        # Get the recruiter and company details from the session and form data
        recruiter = RecruiterService.get_recruiter_by_id()
        recruiter_id = session['user']['recruiter_id']
        company_id = recruiter.company_id
        
        # Extract form data
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
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        jobpost_url = request.form['jobpost_url']
        work_rights = request.form.getlist('work_rights')

        # Call the add_job method of RecruiterService
        recruiter_service.add_job(recruiter_id, company_id, title, description, specialization,
                                   job_type, industry, salary_range, salary_type, work_location,
                                   min_experience_years, experience_level, city,
                                   state, country, jobpost_url, work_rights)

        return jsonify({"message": "Job added successfully"})
    
@recruiter_blueprint.route('/jobs_by_recruiter')
def get_all_jobs_by_recruiter():
    """
    Route for retrieving all job posts by a recruiter.
    
    Returns:
        - Rendered 'recruiter_jobs.html' template with a list of job posts.
        - 401 Unauthorized error if the user is not a recruiter.
    """
    if session['user']['type'] != "recruiter":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        recruiter_id = session['user']['recruiter_id']
        print(f"recruiter_id: {recruiter_id}")
        recruiter_service = RecruiterService()
        jobs_service = JobsService()
        recruiter_jobs = recruiter_service.get_all_jobs_by_recruiter(recruiter_id)
        
        # Fetch company names for each job
        for job in recruiter_jobs:
            company = jobs_service.get_company_by_id(job.company_id)
            job.company_name = company.name if company else "N/A"
        
        print(f"recruiter_jobs: {recruiter_jobs}")
        return render_template('recruiter_jobs.html', jobs=recruiter_jobs)
    
# Update Job Route
@recruiter_blueprint.route('/update_job/<int:job_id>', methods=['GET', 'POST', 'PUT', 'OPTIONS'])
def update_job(job_id):
    """
    Route for updating an existing job post.
    
    GET: Renders the 'update_job.html' template with the job details.
    POST: Extracts form data and calls the 'update_job' method of the RecruiterService.
    
    Returns:
        - For GET: Rendered 'update_job.html' template.
        - For POST: JSON response with a success message.
        - 401 Unauthorized error if the user is not a recruiter or does not have access to the job post.
        - 404 Not Found error if the job post does not exist.
    """
    if 'user' not in session or session['user']['type'] != 'recruiter':
        return jsonify({"error": "Unauthorized access"}), 401
    
    recruiter_id = session['user']['recruiter_id']
    recruiter_service = RecruiterService()
    job_service = JobsService()
    job_post = job_service.get_job_by_id(job_id)

    if not job_post or job_post.recruiter_id != recruiter_id:
        return "Job not found or unauthorized", 404

    if request.method == 'POST':
        data = {
            'title': request.form['title'],
            'description': request.form['description'],
            'specialization': request.form['specialization'],
            'job_type': request.form['job_type'],
            'industry': request.form['industry'],
            'salary_range': request.form['salary_range'],
            'salary_type': request.form['salary_type'],
            'work_location': request.form['work_location'],
            'min_experience_years': request.form['min_experience_years'],
            'experience_level': request.form['experience_level'],
            'tech_stack': request.form['tech_stack'],
            'city': request.form['city'],
            'state': request.form['state'],
            'country': request.form['country'],
            'jobpost_url': request.form['jobpost_url']
        }
        updated_job = recruiter_service.update_job(job_id, data)
        if updated_job:
            return jsonify({"message": "Job updated successfully"})
        else:
            return "Job not found", 404

    # Render the update_job.html template with the job details
    return render_template('update_job.html', job=job_post, job_id=job_id)

@recruiter_blueprint.route('/add_company_and_recruiter', methods=['GET', 'POST'])
def add_company_and_recruiter():
    """
    Route for adding a new company and recruiter.
    
    GET: Renders the 'add_company_and_recruiter.html' template.
    POST: Extracts form data and adds a new company and recruiter to the database.
    
    Returns:
        - For GET: Rendered 'add_company_and_recruiter.html' template.
        - For POST: Redirect to a success page.
    """
    if request.method == 'POST':
        company_name = request.form['company_name']
        website_url = request.form['website_url']
        
        # Add company details to the database
        new_company = Company(name=company_name, website_url=website_url)
        db.session.add(new_company)
        db.session.commit()
        
        # Get the company_id of the newly added company
        company_id = new_company.company_id
        
        # Add recruiter details to the database
        is_direct_recruiter = request.form['is_direct_recruiter'] == 'True'
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        password = request.form['password']  # Note: You should hash the password
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        
        new_recruiter = Recruiter(
            company_id=company_id,
            is_direct_recruiter=is_direct_recruiter,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=password,
            city=city,
            state=state,
            country=country
        )
        
        db.session.add(new_recruiter)
        db.session.commit()
        
        return redirect(url_for('some_success_page'))
    
    return render_template('add_company_and_recruiter.html')