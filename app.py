from flask import Flask, jsonify, render_template, request, session, redirect, url_for, send_from_directory, current_app
from flask_session import Session
from redis import Redis, RedisError
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY
from routes.auth_routes import auth_blueprint
from routes.job_routes import job_blueprint
from routes.recruiter_routes import recruiter_blueprint
from routes.seeker_routes import seeker_blueprint
from extensions import db, bcrypt, migrate
import json
from routes.auth_routes import webapp_secret_key
import logging
from flask_cors import CORS
from models import Job, Company
from sqlalchemy import and_, func, or_ 
from flask_caching import Cache
from routes.job_routes import company_logos
from datetime import datetime, timedelta
from routes.job_routes import JobsService

app = Flask(__name__)
# Update CORS configuration
# CORS(app, supports_credentials=True)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)
app.logger.setLevel(logging.INFO)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app)

app.register_blueprint(auth_blueprint)
app.register_blueprint(job_blueprint)
app.register_blueprint(recruiter_blueprint)
app.register_blueprint(seeker_blueprint)

# Flask-Session configuration
app.config['SECRET_KEY'] = SECRET_KEY
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379, db=0)
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

# Redis Caching Configuration
app.config['CACHE_TYPE'] = 'RedisCache'
app.config['CACHE_REDIS_HOST'] = 'localhost'
app.config['CACHE_REDIS_PORT'] = 6379
app.config['CACHE_REDIS_DB'] = 0
app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
app.config['CACHE_DEFAULT_TIMEOUT'] = 300

cache = Cache(app)

Session(app)

# Set up the database tables
with app.app_context():
    db.create_all()  # This will create all tables based on your models

app.secret_key = webapp_secret_key

app.config.update(
    SESSION_COOKIE_SECURE=True,
    SESSION_COOKIE_HTTPONLY=True,
    SESSION_COOKIE_SAMESITE='None',
)

@app.route('/')
def home():
    user_logged_in = 'user' in session
    if user_logged_in:
        print(session.get('user').get("userinfo").get('name'))
        user_type = session['user']['type'] in session
        print(f"User Type: {session['user']['type']}")
        print("User in session")
    else:
        print("User not in session")
        # return jsonify({"message": "Unauthorized access"}), 401
    return render_template('index.html', user_logged_in=user_logged_in)

@app.route("/check-session", methods=["GET"])
def check_session():
    if 'user' in session:
        # print(f"Session data in check-session: {session}")
        print(f"Session data in check-session: {session['user']['userinfo']['name']}")
        print(f"Session Type in check-session: {session['user']['type']}")
        return jsonify(session['user'])
    else:
        print("No user in session in check-session")
        return jsonify({})

# @app.route('/bookmark_job', methods=['GET', 'POST'])
# # # @requires_auth
# def bookmark_job():
#     if 'user' not in session:
#         print('user not in session!')
#         return jsonify({"error": "Unauthorized access"}), 401
#     else:
#         print('user in session')
        
#         job_id = request.json['jobid']
#         if type(job_id) is not int:
#             print("Invalid job id: ")
#             print(type(job_id))
#             return jsonify({"error": "Invalid job ID"}), 400
        
#         if session['user']['type'] == "recruiter":
#             print("Unauthorized access: Cannot Bookmark Job as a Recruiter")
#             return jsonify({"error": "Unauthorized access"}), 401
        
#         else:  
#             seeker_id = session['user']['uid'];  
#             if seeker_id is None:
#                 return jsonify({"error": "No UserId found"}), 400
#             else:
#                 userid = seeker_id
#                 print(f"userid: {userid}")
#                 print("job_id: ", (job_id))
#                 jobs_service = JobsService()
#                 jobs_service.bookmark_job(userid, (job_id))
#                 return jsonify({"message": "Job Bookmaked successfully"})

# Instant Full-Text Search Endpoint
@app.route('/instant_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def instant_search_jobs():
    query = request.args.get('query', '')
    if query:
        search_query = func.plainto_tsquery('english', query)
        jobs_query = Job.query.filter(Job.search_vector.op('@@')(search_query)).join(Company, Job.company_id == Company.company_id).add_columns(
            Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country, Job.salary_range, Job.created_at, Job.experience_level, Company.name.label('company_name'))
        jobs = jobs_query.all()
        results = [{
            'job_id': job.job_id,
            'title': job.title,
            'company': job.company_name,
            'location': f"{job.city}, {job.state}",
            'city': job.city,
            'country': job.country,
            'salary_range': job.salary_range,
            'created_at': job.created_at.strftime('%Y-%m-%d'),
            'experience_level': job.experience_level,
            'logo': company_logos.get(job.company_name.lower(), ''),
            'specialization': job.specialization
            # 'new': job.created_at >= datetime.datetime.utcnow() - datetime.timedelta(days=7)
        } for job in jobs]
        return jsonify({
            'total': len(results),
            'results': results
        })
    else:
        return jsonify({
            'total': 0,
            'results': []
        })

# Filtered Search Endpoint
@app.route('/filtered_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def filtered_search_jobs():
    specialization = request.args.get('specialization')
    experience_level = request.args.get('experience_level')
    min_experience_years = request.args.get('min_experience_years')
    work_location = request.args.get('work_location')
    industry = request.args.get('industry')
    salary_range = request.args.get('salary_range')
    city = request.args.get('city')
    tech_stack = request.args.get('tech_stack')

    jobs_query = Job.query

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

    jobs = jobs_query.join(Company, Job.company_id == Company.company_id).add_columns(
        Job.job_id, Job.title, Job.description, Job.specialization, Job.salary_range, Job.city, Job.state, Job.country, Job.salary_range, Job.created_at, Job.experience_level, Company.name.label('company_name')).all()

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
        'logo': company_logos.get(job.company_name.lower(), ''),
        'specialization': job.specialization
    } for job in jobs]

    return jsonify({
        'total': len(results),
        'results': results
    })

@app.before_request
def before_request():
    headers = {'Access-Control-Allow-Origin': '*',
               'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
               'Access-Control-Allow-Headers': 'Content-Type'}
    if request.method.lower() == 'options':
        return jsonify(headers), 200



@app.errorhandler(RedisError)
def handle_redis_error(error):
    app.logger.error(f"Redis error encountered: {error}")
    return "A problem occurred with our Redis service. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)


# from flask import Flask, jsonify, render_template, request, session, redirect, url_for, send_from_directory, current_app
# from flask_session import Session
# from redis import Redis, RedisError
# from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY
# from routes.auth_routes import auth_blueprint
# from routes.job_routes import job_blueprint
# from routes.recruiter_routes import recruiter_blueprint
# from routes.seeker_routes import seeker_blueprint
# from extensions import db, bcrypt, migrate
# import json
# from routes.auth_routes import webapp_secret_key
# import logging
# from flask_cors import CORS
# from models import Job, Company
# from sqlalchemy import and_, func, or_ 
# from flask_caching import Cache
# from routes.job_routes import company_logos

# # Create a Flask application instance
# app = Flask(__name__)

# # Apply CORS to the entire app
# CORS(app)

# # Configure the database connection
# app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
# app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# # Set the logging level to INFO
# app.logger.setLevel(logging.INFO)

# # Initialize extensions with the app
# db.init_app(app)
# bcrypt.init_app(app)
# migrate.init_app(app, db)

# # Register blueprints
# app.register_blueprint(auth_blueprint)
# app.register_blueprint(job_blueprint)
# app.register_blueprint(recruiter_blueprint)
# app.register_blueprint(seeker_blueprint)

# # Flask-Session configuration
# app.config['SECRET_KEY'] = SECRET_KEY
# app.config['SESSION_TYPE'] = 'redis'
# app.config['SESSION_PERMANENT'] = True
# app.config['SESSION_USE_SIGNER'] = True
# app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379, db=0)
# app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

# # Redis Caching Configuration
# app.config['CACHE_TYPE'] = 'RedisCache'
# app.config['CACHE_REDIS_HOST'] = 'localhost'
# app.config['CACHE_REDIS_PORT'] = 6379
# app.config['CACHE_REDIS_DB'] = 0
# app.config['CACHE_REDIS_URL'] = 'redis://localhost:6379/0'
# app.config['CACHE_DEFAULT_TIMEOUT'] = 300

# # Initialize the cache
# cache = Cache(app)

# # Initialize the session
# Session(app)

# # Set up the database tables
# with app.app_context():
#     db.create_all()  # This will create all tables based on your models

# # Set the secret key for the app
# app.secret_key = webapp_secret_key

# # Home route
# @app.route('/')
# def home():
#     # Check if a user is logged in
#     user_logged_in = 'user' in session
#     if user_logged_in:
#         print(session.get('user').get("userinfo").get('name'))
#         user_type = session['user']['type'] in session
#         print(f"User Type: {session['user']['type']}")
#         print("User in session")
#     else:
#         print("User not in session")
#     return render_template('index.html', user_logged_in=user_logged_in)

# @app.route("/check-session", methods=["GET"])
# def check_session():
#     if 'user' in session:
#         return jsonify({
#             'is_logged_in': True,
#             'user_name': session['user'].get('userinfo').get('name')
#         })
#     else:
#         return jsonify({
#             'is_logged_in': False,
#             'user_name': None
#         })

# # Instant search jobs route
# @app.route('/instant_search_jobs', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
# def instant_search_jobs():
#     """
#     Performs an instant search for jobs based on the provided query.
#     The results are cached for 60 seconds.
#     """
#     query = request.args.get('query', '')
#     if query:
#         # Construct the search query
#         search_query = func.plainto_tsquery('english', query)
#         jobs_query = Job.query.filter(
#             or_(
#                 # Search for jobs where the search vector matches the search query
#                 Job.search_vector.op('@@')(search_query),
#                 # Search for jobs where the company name contains the search query (case-insensitive)
#                 Company.name.ilike(f'%{query}%')
#             )).join(
#             # Join the Job and Company tables based on the company_id foreign key
#             Company, Job.company_id == Company.company_id).add_columns(
#             # Select the following columns from the Job and Company tables
#             Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country,
#             Job.salary_range, Job.created_at, Job.experience_level, Company.name.label('company_name')
#         )
#         # Execute the query and fetch all results
#         jobs = jobs_query.all()
#         # Format the results
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
#             'logo': company_logos.get(job.company_name.lower(), ''),
#         } for job in jobs]
#         return jsonify({
#             'total': len(results),
#             'results': results
#         })
#     else:
#         return jsonify({
#             'total': 0,
#             'results': []
#         })

# # Filtered search jobs route
# @app.route('/filtered_search_jobs', methods=['GET'])
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
#     tech_stack = request.args.get('tech_stack')

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
#         Job.created_at, Job.experience_level, Company.name.label('company_name')).all()

#     results = [{
#         'job_id': job.job_id,
#         'title': job.title,
#         'company': job.company_name,
#         'city': job.city,
#         'location': f"{job.city}, {job.state}",
#         'country': job.country,
#         'salary_range': job.salary_range,
#         'created_at': job.created_at.strftime('%Y-%m-%d'),
#         'experience_level': job.experience_level,
#         'specialization': job.specialization,
#         'logo': company_logos.get(job.company_name.lower(), ''),
#     } for job in jobs]

#     return jsonify({
#         'total': len(results),
#         'results': results
#     })

# # Error handler for Redis errors
# @app.errorhandler(RedisError)
# def handle_redis_error(error):
#     """
#     Handles Redis errors and logs the error message.
#     """
#     app.logger.error(f"Redis error encountered: {error}")
#     return "A problem occurred with our Redis service. Please try again later.", 500

# if __name__ == '__main__':
#     app.run(debug=True)