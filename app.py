from flask import Flask, jsonify, render_template, request
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from db_setup import setup_tables
from service.jobs_service import JobsService
from service.jobseeker_service import SeekerService
from service.recruiter_service import RecruiterService
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

# Set up the database tables
with app.app_context():
    setup_tables()

@app.route('/')
def home():
    return render_template('index.html')

@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
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

        jobs_service.add_job(recruiter_id, company_id, title, description, specialization,
                             job_type, industry, salary_range, salary_type, work_location,
                             min_experience_years, experience_level, tech_stack, city,
                             state, country, jobpost_url, work_rights)

        return jsonify({"message": "Job added successfully"})

@app.route('/add_recruiter', methods=['GET', 'POST'])
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

@app.route('/add_company', methods=['GET', 'POST'])
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

@app.route('/add_seeker', methods=['GET', 'POST'])
def add_seeker():
    if request.method == 'POST':
        # Extract form data and call the add_seeker method of SeekerService
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']

        seeker_service = SeekerService()
        seeker_service.add_seeker(first_name, last_name, email, city, state, country)

        return "Job Seeker added successfully!"
    else:
        return render_template('add_seeker.html')

# Apply to a Job
@app.route('/apply_to_job', methods=['POST'])
def apply_to_job():
    userid = request.form['userid']
    jobid = request.form['jobid']

    jobs_service = JobsService()
    jobs_service.apply_to_job(userid, jobid)

    return jsonify({"message": "Job application submitted successfully"})

# Bookmark a job
@app.route('/bookmark_job', methods=['POST'])
def bookmark_job():
    userid = request.form['userid']
    jobid = request.form['jobid']

    jobs_service = JobsService()
    jobs_service.bookmark_job(userid, jobid)

    return jsonify({"message": "Job bookmarked successfully"})

@app.route('/available_jobs')
def available_jobs():
    jobs_service = JobsService()
    jobs = jobs_service.get_available_jobs()
    return render_template('available_jobs.html', jobs=jobs)

# Route to filter jobs based on certain criteria:
@app.route('/filter_jobs')
def filter_jobs():
    company_id = request.args.get('company')
    experience_level = request.args.get('experience_level')
    industry = request.args.get('industry')
    
    jobs_service = JobsService()
    filtered_jobs = jobs_service.filter_jobs(company_id, experience_level, industry)
    
    return render_template('filtered_jobs.html', jobs=filtered_jobs)

if __name__ == '__main__':
    app.run(debug=True)