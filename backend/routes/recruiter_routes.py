from flask import Blueprint, render_template, request, redirect, url_for, session, jsonify, current_app
from service.recruiter_service import RecruiterService
from service.jobs_service import JobsService
from models import Recruiter, Company, Job
from extensions import db
from flask_cors import CORS
from werkzeug.utils import secure_filename
import os


# Create a Blueprint for recruiter-related routes
recruiter_blueprint = Blueprint('recruiter', __name__)
CORS(recruiter_blueprint, supports_credentials=True, resources={r'/*': {'origins': 'http://localhost'}})

# Add Recruiter Route
@recruiter_blueprint.route('/api/add_recruiter', methods=['GET', 'POST'])
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
@recruiter_blueprint.route('/api/add_company', methods=['GET', 'POST'])
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

@recruiter_blueprint.route('/api/add_job', methods=['POST'])
def add_job():
    """
    Route for adding a new job post.
    
    POST: Extracts JSON data and calls the 'add_job' method of the RecruiterService.
    
    Returns:
        - JSON response with a success message.
    """
    recruiter_service = RecruiterService()
    
    if request.method == 'POST':
        if 'user' not in session or session['user']['type'] != 'recruiter':
            return jsonify({"error": "Unauthorized access"}), 401

        data = request.json  # Expecting JSON data
        recruiter_id = session['user']['recruiter_id']
        recruiter = Recruiter.query.get(recruiter_id)
        company_id = recruiter.company_id
        
        # Extract form data from JSON
        title = data['title']
        description = data['description']
        specialization = data['specialization']
        job_type = data['job_type']
        industry = data['industry']
        salary_range = data['salary_range']
        salary_type = data['salary_type']
        work_location = data['work_location']
        min_experience_years = data['min_experience_years']
        experience_level = data['experience_level']
        city = data['city']
        state = data['state']
        country = data['country']
        jobpost_url = data['jobpost_url']
        work_rights = data['work_rights']

        # Call the add_job method of RecruiterService
        new_job, error = recruiter_service.add_job(recruiter_id, company_id, title, description, specialization,
                                   job_type, industry, salary_range, salary_type, work_location,
                                   min_experience_years, experience_level, city,
                                   state, country, jobpost_url, work_rights)

        if new_job:
            return jsonify({"message": "Job added successfully", "job_id": new_job.job_id}), 200
        else:
            return jsonify({"error": f"Failed to add job: {error}"}), 400

    return jsonify({"error": "Invalid request method"}), 405

@recruiter_blueprint.route('/api/jobs_by_recruiter')
def get_all_jobs_by_recruiter():
    if session['user']['type'] != "recruiter":
        return jsonify({"error": "Unauthorized access"}), 401
    else:
        recruiter_id = session['user']['recruiter_id']
        recruiter_service = RecruiterService()
        jobs_service = JobsService()
        recruiter_jobs = recruiter_service.get_all_jobs_by_recruiter(recruiter_id)
        # Build the response data
        response_data = []
        for job in recruiter_jobs:
            company = jobs_service.get_company_by_id(job.company_id)
            company_logo=company.logo_url
            if company_logo: 
                    company_logo = f"http://127.0.0.1:4040/uploads/{os.path.basename(company.logo_url)}"

            print(f"compay logo: {company.logo_url}")

            
            job_data = {
                "job_id": job.job_id,
                "recruiter_id": job.recruiter_id,
                "company_id": job.company_id,
                "title": job.title,
                "description": job.description,
                "specialization": job.specialization,
                "job_type": job.job_type,
                "industry": job.industry,
                "salary_range": job.salary_range,
                "salary_type": job.salary_type,
                "work_location": job.work_location,
                "min_experience_years": job.min_experience_years,
                "experience_level": job.experience_level,
                "tech_stack": job.tech_stack,
                "city": job.city,
                "state": job.state,
                "country": job.country,
                "expiry_date": job.expiry_date,
                "jobpost_url": job.jobpost_url,
                "work_rights": job.work_rights,
                "created_at": job.created_at,
                "updated_at": job.updated_at,
                "logo": company_logo,
                "company_name": company.name if company else "N/A",
            }
            response_data.append(job_data)
        
        return jsonify(response_data)

@recruiter_blueprint.route('/api/job/<int:job_id>', methods=['GET'])
def get_job_by_id(job_id):
    job_service = JobsService()
    job_post = job_service.get_job_by_id(job_id)
    if job_post:
        company = job_service.get_company_by_id(job_post.company_id)
        job_data = {
            "job_id": job_post.job_id,
            "recruiter_id": job_post.recruiter_id,
            "company_id": job_post.company_id,
            "title": job_post.title,
            "description": job_post.description,
            "specialization": job_post.specialization,
            "job_type": job_post.job_type,
            "industry": job_post.industry,
            "salary_range": job_post.salary_range,
            "salary_type": job_post.salary_type,
            "work_location": job_post.work_location,
            "min_experience_years": job_post.min_experience_years,
            "experience_level": job_post.experience_level,
            "tech_stack": job_post.tech_stack,
            "city": job_post.city,
            "state": job_post.state,
            "country": job_post.country,
            "expiry_date": job_post.expiry_date,
            "jobpost_url": job_post.jobpost_url,
            "work_rights": job_post.work_rights,
            "created_at": job_post.created_at,
            "updated_at": job_post.updated_at,
            "company_name": company.name if company else "N/A",
        }
        return jsonify(job_data)
    else:
        return jsonify({"error": "Job not found"}), 404


# Update Recruiter Data
@recruiter_blueprint.route('/api/register/employer/info', methods=['POST'])
def update_recruiter_info():
    if "user" in session and session["user"]["type"] == "recruiter":
        recruiter_id = session["user"]["recruiter_id"]
        recruiter = Recruiter.query.get(recruiter_id)

        if recruiter:
            data = request.get_json()
            recruiter.first_name = data.get('firstName')
            recruiter.last_name = data.get('lastName')
            recruiter.position = data.get('position')
            db.session.commit()

            return jsonify({"message": "Recruiter info updated successfully"}), 200
        else:
            return jsonify({"message": "Recruiter not found"}), 404
    else:
        return jsonify({"message": "Unauthorized"}), 401

# Update Job Route
@recruiter_blueprint.route('/api/update_job/<int:job_id>', methods=['POST'])
@recruiter_blueprint.route('/api/update_job/<int:job_id>', methods=['POST'])
def update_job(job_id):
    """
    Route for updating an existing job post.
    
    POST: Extracts JSON data and calls the 'update_job' method of the RecruiterService.
    POST: Extracts JSON data and calls the 'update_job' method of the RecruiterService.
    
    Returns:
        - JSON response with a success message.
        - JSON response with a success message.
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
        return jsonify({"error": "Job not found or unauthorized"}), 404
        return jsonify({"error": "Job not found or unauthorized"}), 404

    data = request.get_json()
    updated_data = {
        'title': data['title'],
        'description': data['description'],
        'specialization': data['specialization'],
        'job_type': data['job_type'],
        'industry': data['industry'],
        'salary_range': data['salary_range'],
        'salary_type': data['salary_type'],
        'work_location': data['work_location'],
        'min_experience_years': data['min_experience_years'],
        'experience_level': data['experience_level'],
        'tech_stack': data['tech_stack'],
        'city': data['city'],
        'state': data['state'],
        'country': data['country'],
        'jobpost_url': data['jobpost_url'],
        'work_rights': data['work_rights']
    }
    updated_job = recruiter_service.update_job(job_id, updated_data)
    if updated_job:
        return jsonify({"message": "Job updated successfully"})
    else:
        return jsonify({"error": "Job not found"}), 404
    data = request.get_json()
    updated_data = {
        'title': data['title'],
        'description': data['description'],
        'specialization': data['specialization'],
        'job_type': data['job_type'],
        'industry': data['industry'],
        'salary_range': data['salary_range'],
        'salary_type': data['salary_type'],
        'work_location': data['work_location'],
        'min_experience_years': data['min_experience_years'],
        'experience_level': data['experience_level'],
        'tech_stack': data['tech_stack'],
        'city': data['city'],
        'state': data['state'],
        'country': data['country'],
        'jobpost_url': data['jobpost_url'],
        'work_rights': data['work_rights']
    }
    updated_job = recruiter_service.update_job(job_id, updated_data)
    if updated_job:
        return jsonify({"message": "Job updated successfully"})
    else:
        return jsonify({"error": "Job not found"}), 404

@recruiter_blueprint.route('/api/add_company_and_recruiter', methods=['GET', 'POST'])
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

@recruiter_blueprint.route('/api/companies', methods=['GET'])
def get_companies():
    companies = Company.query.all()
    company_list = [{"name": company.name} for company in companies]
    return jsonify(company_list), 200


@recruiter_blueprint.route('/api/register/employer/update_company', methods=['POST'])
def update_recruiter_company():
    if "user" in session and session["user"]["type"] == "recruiter":
        recruiter_id = session["user"]["recruiter_id"]
        recruiter = Recruiter.query.get(recruiter_id)

        if recruiter:
            data = request.get_json()
            company_name = data.get('company')
            company = Company.query.filter_by(name=company_name).first()

            if company:
                recruiter.company_id = company.id
                db.session.commit()

                return jsonify({"message": "Recruiter company updated successfully"}), 200
            else:
                return jsonify({"message": "Company not found"}), 404
        else:
            return jsonify({"message": "Recruiter not found"}), 404
    else:
        return jsonify({"message": "Unauthorized"}), 401
    
# recruiter_routes.py
@recruiter_blueprint.route('/api/register/employer/create_company', methods=['POST'])
def create_company():
    if "user" in session and session["user"]["type"] == "recruiter":
        recruiter_id = session["user"]["recruiter_id"]
        recruiter = Recruiter.query.get(recruiter_id)

        if recruiter:
            data = request.form

            # Handle file upload for the logo
            logo_file = request.files.get('logo')
            logo_path = None
            if logo_file:
                logo_filename = secure_filename(logo_file.filename)
                logo_path = os.path.join(current_app.config['UPLOAD_FOLDER'], logo_filename)
                logo_file.save(logo_path)

            new_company = Company(
                name=data.get('employerName'),
                website_url=data.get('employerWebsite'),
                country=data.get('country'),
                size=data.get('employerSize'),
                address=data.get('employerAddress'),
                description=data.get('employerDescription'),
                logo_url=logo_path  # Assuming you have a field for logo URL
            )
            db.session.add(new_company)
            db.session.commit()

            recruiter.company_id = new_company.company_id
            db.session.commit()

            return jsonify({"message": "Company created and recruiter updated successfully"}), 200
        else:
            return jsonify({"message": "Recruiter not found"}), 404
    else:
    
@recruiter_blueprint.route('/api/remove-job-by-recruiter/<int:job_id>', methods=['POST'])
def remove_job(job_id):
    if "user" in session and session["user"]["type"] == "recruiter":
        recruiter_id = session["user"]["recruiter_id"]
        job_service = JobsService()
        recruiter_service = RecruiterService()
        job_post = job_service.get_job_by_id(job_id)

        if not job_post or job_post.recruiter_id != recruiter_id:
            return jsonify({"error": "Job not found or unauthorized"}), 404
        
        if recruiter_service.remove_job(job_id, recruiter_id):
            return jsonify({"message": "Job post removed successfully"}), 200
        else:
            return jsonify({"error": "Job not found or unauthorized"}), 404
    else:
        return jsonify({"message": "Unauthorized"}), 401