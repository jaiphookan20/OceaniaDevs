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

app = Flask(__name__)
CORS(app)  # Apply CORS to the entire app
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.INFO)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

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
    return render_template('index.html', user_logged_in=user_logged_in)

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
    else:
        return jsonify({
            'total': 0,
            'results': []
        })

@app.route('/filtered_search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def filtered_search_jobs():
    specialization = request.args.get('specialization')
    experience_level = request.args.get('experience_level')
    work_location = request.args.get('work_location')
    industry = request.args.get('industry')
    salary_range = request.args.get('salary_range')
    tech_stack = request.args.get('tech_stack')
    company = request.args.get('company')

    jobs_query = Job.query

    if specialization:
        jobs_query = jobs_query.filter(Job.specialization == specialization)
    if experience_level:
        jobs_query = jobs_query.filter(Job.experience_level == experience_level)
    if work_location:
        jobs_query = jobs_query.filter(or_(Job.city == work_location, Job.state == work_location, Job.country == work_location))
    if industry:
        jobs_query = jobs_query.filter(Job.industry == industry)
    if salary_range:
        jobs_query = jobs_query.filter(Job.salary_range == salary_range)
    if company:
        jobs_query = jobs_query.filter(Job.company_id == company)

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
        'specialization': job.specialization,
        'logo': company_logos.get(job.company_name.lower(), ''),
    } for job in jobs]

    return jsonify({
        'total': len(results),
        'results': results
    })

@app.errorhandler(RedisError)
def handle_redis_error(error):
    app.logger.error(f"Redis error encountered: {error}")
    return "A problem occurred with our Redis service. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)
