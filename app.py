from flask import Flask, jsonify, render_template, request
import psycopg2
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD
from db_setup import setup_tables
import logging

app = Flask(__name__)
app.logger.setLevel(logging.INFO)

@app.route('/')
def home():
    return render_template('index.html')


# Set up the database tables
with app.app_context():
    setup_tables()


# GET ALL COMPANIES: 
@app.route('/get_companies', methods=['GET'])
def get_companies():
    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        query = """
            select * from companies;
        """
        
        cur.execute(query)
        companies = cur.fetchall()  # Fetch all results

        # Convert the list of tuples into a list of dictionaries
        companies_list = []
        for company in companies:
            companies_list.append({
                'id': company[0],
                'name': company[1],
                'description': company[2],
                # Add more fields as needed
            })

        cur.close()
        conn.close()

        return jsonify(companies_list)  # Return JSON response
    
    except psycopg2.Error as e:
        print(f"Error fetching all companies: {e}")
        return "An error occurred while fetching all the companies"
    
@app.route('/add_job', methods=['GET', 'POST'])
def add_job():
    if request.method == 'GET':
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            # Fetch the list of recruiters and companies
            cur.execute("SELECT recruiter_id, first_name, last_name FROM recruiters")
            recruiters = cur.fetchall()
            cur.execute("SELECT company_id, name FROM companies")
            companies = cur.fetchall()

            cur.close()
            conn.close()

            return render_template('add_job.html', recruiters=recruiters, companies=companies)

        except psycopg2.Error as e:
            app.logger.error(f"Error fetching recruiters and companies: {e}")
            return jsonify({"error": "An error occurred while fetching recruiters and companies"}), 500

    recruiter_id = request.form['recruiter_id']
    company_id = request.form['company_id']
    title = request.form['title']
    description = request.form['description']
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
    work_rights = request.form['work_rights']
    

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        query = """
            INSERT INTO jobs (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights)

        cur.execute(query, values)
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Job added successfully"})

    except psycopg2.Error as e:
        app.logger.error(f"Error inserting job: {e}")
        return jsonify({"error": "An error occurred while adding the job"}), 500

@app.route('/add_recruiter', methods=['GET', 'POST'])
def add_recruiter():
    if request.method == 'GET':
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()

            # Fetch the list of companies
            cur.execute("SELECT company_id, name FROM companies")
            companies = cur.fetchall()

            cur.close()
            conn.close()

            return render_template('add_recruiter.html', companies=companies)

        except psycopg2.Error as e:
            app.logger.error(f"Error fetching companies: {e}")
            return jsonify({"error": "An error occurred while fetching companies"}), 500

    first_name = request.form['first_name']
    last_name = request.form['last_name']
    email = request.form['email']
    password = request.form['password']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']
    company_id = request.form['company_id']
    is_direct_recruiter = request.form['is_direct_recruiter']
    
    # Convert is_direct_recruiter to boolean
    is_direct_recruiter = is_direct_recruiter.lower() == 'true'

    print(first_name, last_name, email, password)

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()

        query = """
            INSERT INTO recruiters (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """
        values = (company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter)

        cur.execute(query, values)
        conn.commit()

        cur.close()
        conn.close()

        return jsonify({"message": "Recruiter added successfully"})

    except psycopg2.Error as e:
        app.logger.error(f"Error inserting recruiter: {e}")
        return jsonify({"error": "An error occurred while adding the recruiter"}), 500

# ADD RECRUITER's COMPANY
@app.route('/add_company', methods=['GET','POST'])
def add_company():
    if request.method == 'GET':
        return render_template('add_company.html')
    name = request.form['name']
    city = request.form['city']
    state = request.form['state']
    country = request.form['country']

    try:
        conn = psycopg2.connect(
            host=DB_HOST,
            database=DB_NAME,
            user=DB_USER,
            password=DB_PASSWORD
        )
        cur = conn.cursor()
        
        query = """
            INSERT INTO companies (name, city, state, country)
            VALUES (%s, %s, %s, %s)
        """
        values = (name, city, state, country)
        
        cur.execute(query, values)
        conn.commit()
        
        cur.close()
        conn.close()
        
        return "Company added successfully!"
        
    except psycopg2.Error as e:
        print(f"Error inserting Company: {e}")
        return "An error occurred while adding the company"


# ADD JOB SEEKER
@app.route('/add_seeker', methods=['GET', 'POST'])
def add_seeker():
    # test test comment
    if request.method == 'POST':
        first_name = request.form['first_name']
        last_name = request.form['last_name']
        email = request.form['email']
        city = request.form['city']
        state = request.form['state']
        country = request.form['country']
        
        try:
            conn = psycopg2.connect(
                host=DB_HOST,
                database=DB_NAME,
                user=DB_USER,
                password=DB_PASSWORD
            )
            cur = conn.cursor()
            
            query = """
                INSERT INTO seekers (first_name, last_name, email, city, state, country)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            values = (first_name, last_name, email, city, state, country)
            
            cur.execute(query, values)
            conn.commit()
            
            cur.close()
            conn.close()
            
            return "Job Seeker added successfully!"
        
        except psycopg2.Error as e:
            print(f"Error inserting seeker: {e}")
            return "An error occurred while adding the seeker"
    
    return render_template('add_seeker.html')

# if __name__ == '__main__':
#     # app.run(debug=True)
