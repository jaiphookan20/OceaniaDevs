from flask import Flask, jsonify, render_template, request, session, redirect, url_for, send_from_directory
from flask_session import Session
from redis import Redis, RedisError
from config import DB_HOST, DB_NAME, DB_USER, DB_PASSWORD, SECRET_KEY
from db_setup import setup_tables
from service.jobs_service import JobsService
from service.seeker_service import SeekerService
from service.recruiter_service import RecruiterService
import logging
from routes.auth_routes import auth_blueprint
from routes.job_routes import job_blueprint
from routes.recruiter_routes import recruiter_blueprint
from routes.seeker_routes import seeker_blueprint
from flask_migrate import Migrate
from flask_bcrypt import Bcrypt
from extensions import db, bcrypt, migrate

app = Flask(__name__)
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
app.config['SECRET_KEY']= SECRET_KEY
app.config['SESSION_TYPE'] = 'redis'
app.config['SESSION_PERMANENT'] = True
app.config['SESSION_USE_SIGNER'] = True
app.config['SESSION_REDIS'] = Redis(host='localhost', port=6379, db=0)
app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

Session(app)

# Set up the database tables
with app.app_context():
    print(bcrypt.generate_password_hash('test').decode('utf-8'))
    db.create_all()  # This will create all tables based on your models

@app.route('/')
def home():
    return render_template('index.html')

# Serve CSS files from 'templates/css'
@app.route('/<path:name>')
def serve_css(name):
    return send_from_directory('templates/css', name)

# Serve HTML files from 'templates'
@app.route('/<path:name>')
def serve_html(name):
    return send_from_directory('templates', name)

@app.errorhandler(RedisError)
def handle_redis_error(error):
    app.logger.error(f"Redis error encountered: {error}")
    return "A problem occurred with our Redis service. Please try again later.", 500

if __name__ == '__main__':
    app.run(debug=True)