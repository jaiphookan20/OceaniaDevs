from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory, current_app
from flask_session import Session
from redis import Redis, RedisError
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY, TEST_DB_NAME, TEST_DB_USER, TEST_DB_PASSWORD
from routes.auth_routes import auth_blueprint
from routes.job_routes import job_blueprint
from routes.recruiter_routes import recruiter_blueprint
from routes.seeker_routes import seeker_blueprint
from routes.similarity_search_routes import simsearch_blueprint
from extensions import db, bcrypt, migrate
from routes.auth_routes import webapp_secret_key
import logging
from flask_cors import CORS
from dotenv import load_dotenv
import os
from extensions import db
from flask_migrate import Migrate
from extensions import cache
from models import Job, Company, Recruiter

load_dotenv()

app = Flask(__name__)
CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
app.config['CORS_HEADERS'] = 'Content-Type'

# Define the upload subdirectory
UPLOAD_FOLDER = os.path.join('uploads', 'upload_company_logo')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Make sure the entire directory structure exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Use test database if in testing environment
if os.getenv("FLASK_ENV") == "testing":
    print('Running Test DB');
    app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{TEST_DB_USER}:{TEST_DB_PASSWORD}@{DB_HOST}/{TEST_DB_NAME}'
else:
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
# migrate.init_app(app)
migrate = Migrate(app, db)

app.register_blueprint(auth_blueprint)
app.register_blueprint(job_blueprint)
app.register_blueprint(recruiter_blueprint)
app.register_blueprint(seeker_blueprint)
app.register_blueprint(simsearch_blueprint)

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

# cache = Cache(app)
cache.init_app(app)  # Initialize the Cache instance with the app

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

# Home route
@app.route('/')
def home():
    # Check if a user is logged in
    user_logged_in = 'user' in session
    if user_logged_in:
        print(session.get('user').get("userinfo").get('name'))
        user_type = session['user']['type'] in session
        print(f"User Type: {session['user']['type']}")
        print("User in session")
    else:
        print("User not in session")
    return jsonify({"status": "API is running", "user_logged_in": user_logged_in})

@app.route("/api/check-session", methods=["GET"])
def check_session():
    if 'user' in session:
        # print(f"Session data in check-session: {session}")
        print(f"Session data in check-session: {session['user']['userinfo']['name']}")
        print(f"Session Type in check-session: {session['user']['type']}")
        return jsonify(session['user'])
    else:
        print("No user in session in check-session")
        return jsonify({})
    
# Serve the uploaded files
@app.route('/uploads/<path:filename>')
def serve_uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
    
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