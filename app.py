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
from routes.auth_routes import webapp_secret_key;
import logging
from flask_cors import CORS
from models import Job, Company
from sqlalchemy import func
from flask_caching import Cache

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "*"}})
app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.logger.setLevel(logging.INFO)

# Initialize extensions with the app
db.init_app(app)
bcrypt.init_app(app)
migrate.init_app(app, db)

# app.register_blueprint(auth_bp, url_prefix='/') # 👈 new code
app.register_blueprint(auth_blueprint)
app.register_blueprint(job_blueprint)
app.register_blueprint(recruiter_blueprint)
app.register_blueprint(seeker_blueprint)

# Flask-Session configuration
app.config['SECRET_KEY']= SECRET_KEY
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379, db=0)
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

#Redis Caching Configuration
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
    if (user_logged_in):
        print(session.get('user').get("userinfo").get('name'))
        user_type = session['user']['type'] in session
        print(f"User Type: {session['user']['type']}")
        print("User in session")
    else:
        print("User not in session")
        # return jsonify({"message": "Unauthorized access"}), 401
    return render_template('index.html', user_logged_in=user_logged_in)

# @app.route('/search_jobs', methods=['GET'])
# @cache.cached(timeout=60, query_string=True)
# def search_jobs():


@app.route('/search_jobs', methods=['GET'])
@cache.cached(timeout=60, query_string=True)
def search_jobs():
    query = request.args.get('query', '')
    if query:
        # Use plainto_tsquery correctly with the query string
        search_query = func.plainto_tsquery('english', query)
        # Ensure the search vector is matched correctly
        jobs_query = Job.query.filter(Job.search_vector.op('@@')(search_query)).join(Company, Job.company_id == Company.company_id).add_columns(
            Job.job_id, Job.title, Job.description, Job.specialization, Job.city, Job.state, Job.country, Company.name.label('company_name'))
        jobs = jobs_query.all()
        results = [{
            'job_id': job.job_id,
            'title': job.title,
            'description': job.description,
            'specialization': job.specialization,
            'city': job.city,
            'state': job.state,
            'country': job.country,
            'company_name': job.company_name,
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

@app.errorhandler(RedisError)
def handle_redis_error(error):
    app.logger.error(f"Redis error encountered: {error}")
    return "A problem occurred with our Redis service. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)