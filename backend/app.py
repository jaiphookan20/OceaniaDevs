# EXTRA LOGGING TO DEBUG AUTH0 MISMATCH STATE ERROR POST LOGIN THROUGH AUTH0
from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory, current_app
from flask_session import Session
from redis import Redis, RedisError
from routes.auth_routes import auth_blueprint, init_auth
from routes.job_routes import job_blueprint
from routes.recruiter_routes import recruiter_blueprint
from routes.seeker_routes import seeker_blueprint
from matching.similarity_search_routes import simsearch_blueprint
from extensions import db, bcrypt, migrate, cache
from routes.auth_routes import webapp_secret_key
import logging
from flask_cors import CORS
from dotenv import load_dotenv
import os
from flask_migrate import Migrate
from models import Job, Company, Recruiter, Seeker, JobTechnology, Technology, TechnologyAlias, Bookmark, Application, state_enum, country_enum, job_type_enum, industry_enum, salary_range_enum
from matching.custom_types import Vector
from admin_views import (
    SecureAdminIndexView, SeekerView, RecruiterView, 
    CompanyView, JobView, ApplicationView, DashboardView, StatisticsView, ReportView, TechnologyAliasView, JobTechnologyView, TechnologiesView
)
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView
from flask import render_template


load_dotenv()

class SecureModelView(ModelView):
    def is_accessible(self):
        return 'user' in session and session['user'].get('type') == 'recruiter'

    def inaccessible_callback(self, name, **kwargs):
        return render_template('admin/unauthorized.html'), 403

def create_app():
    # app = Flask(__name__)
    app = Flask(__name__, template_folder='templates')
    CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
    app.config['CORS_HEADERS'] = 'Content-Type'

    # Set up logging
    logging.basicConfig(level=logging.DEBUG)
    app.logger.setLevel(logging.DEBUG)
    file_handler = logging.FileHandler('app.log')
    file_handler.setLevel(logging.DEBUG)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(formatter)
    app.logger.addHandler(file_handler)

    app.logger.info(f"AUTH0_DOMAIN: {os.getenv('AUTH0_DOMAIN')}")
    app.logger.info(f"AUTH0_CLIENT_ID: {os.getenv('AUTH0_CLIENT_ID')}")
    app.logger.info(f"AUTH0_CLIENT_SECRET: {os.getenv('AUTH0_CLIENT_SECRET')}")

    # Define the upload subdirectory
    UPLOAD_FOLDER = os.path.join('uploads', 'upload_company_logo')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)

    # Database configuration
    DB_HOST = os.environ.get('DB_HOST', 'localhost')
    DB_NAME = os.environ.get('DB_NAME', 'job_board')
    DB_USER = os.environ.get('DB_USER', 'jai')
    DB_PASSWORD = os.environ.get('DB_PASSWORD', 'techboard')

    # Redis configuration
    REDIS_HOST = os.environ.get('REDIS_HOST', 'redis')
    REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

    # Use test database if in testing environment
    if os.getenv("FLASK_ENV") == "testing":
        app.logger.info('Running Test DB')
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}_test'
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    app.config.update(
        SESSION_COOKIE_SECURE=False,  # Set to False since we're not using HTTPS
        SESSION_COOKIE_HTTPONLY=True,
        SESSION_COOKIE_SAMESITE='Lax',
    )

    # Initialize extensions with the app
    db.init_app(app)
    bcrypt.init_app(app)
    migrate.init_app(app, db)

    # Register ENUM types
    def create_enums():
        with app.app_context():
            db.create_all()
            app.logger.info("Database tables created successfully.")
            for enum in [state_enum, country_enum, job_type_enum, industry_enum, salary_range_enum]:
                enum.create(bind=db.engine, checkfirst=True)

    create_enums()

    # Register blueprints
    app.register_blueprint(auth_blueprint)
    app.register_blueprint(job_blueprint)
    app.register_blueprint(recruiter_blueprint)
    app.register_blueprint(seeker_blueprint)
    app.register_blueprint(simsearch_blueprint)

    # Flask-Session configuration
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', webapp_secret_key)
    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = True
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_REDIS'] = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
    app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

    # Redis Caching Configuration
    app.config['CACHE_TYPE'] = 'RedisCache'
    app.config['CACHE_REDIS_HOST'] = REDIS_HOST
    app.config['CACHE_REDIS_PORT'] = REDIS_PORT
    app.config['CACHE_REDIS_DB'] = 0
    app.config['CACHE_REDIS_URL'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
    app.config['CACHE_DEFAULT_TIMEOUT'] = 300

    cache.init_app(app)
    Session(app)

    with app.app_context():
        init_auth(app);

    # Test Redis connection
    try:
        redis_client = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
        redis_client.ping()
        app.logger.info(f"Successfully connected to Redis at {REDIS_HOST}:{REDIS_PORT}")
    except Exception as e:
        app.logger.error(f"Failed to connect to Redis at {REDIS_HOST}:{REDIS_PORT}: {str(e)}")

    # Initialize Flask-Admin
    admin = Admin(app, name='Job Board Admin', template_mode='bootstrap3', index_view=SecureAdminIndexView())

    # Add views for each model
    admin.add_view(SeekerView(Seeker, db.session, name='Seekers', endpoint='admin_seekers'))
    admin.add_view(RecruiterView(Recruiter, db.session, name='Recruiters', endpoint='admin_recruiters'))
    admin.add_view(CompanyView(Company, db.session, name='Companies', endpoint='admin_companies'))
    admin.add_view(JobView(Job, db.session, name='Jobs', endpoint='admin_jobs'))
    admin.add_view(ApplicationView(Application, db.session, name='Applications', endpoint='admin_applications'))
    admin.add_view(TechnologiesView(Technology, db.session, name='Technologies', endpoint='admin_technologies'))
    admin.add_view(TechnologyAliasView(TechnologyAlias, db.session, name='Technology Aliases', endpoint='admin_technology_aliases'))
    admin.add_view(JobTechnologyView(JobTechnology, db.session, name='Job Technologies', endpoint='admin_job_technologies'))

    # Add custom views
    admin.add_view(DashboardView(name='Dashboard', endpoint='admin_dashboard'))
    admin.add_view(StatisticsView(name='Statistics', endpoint='admin_statistics'))
    admin.add_view(ReportView(name='Reports', endpoint='admin_reports'))

    @app.route('/')
    def home():
        user_logged_in = 'user' in session
        if user_logged_in:
            app.logger.info(f"User logged in: {session.get('user').get('userinfo').get('name')}")
            app.logger.info(f"User Type: {session['user']['type']}")
        else:
            app.logger.info("User not in session")
        return jsonify({"status": "API is running", "user_logged_in": user_logged_in})
    
    # Serve HTML files from 'templates'
    @app.route('/<path:name>')
    def serve_html(name):
        return send_from_directory('templates', name)
    
    @app.route('/api/admin', methods=["GET"])
    def admin_index():
        app.logger.debug("Admin route hit")
        if 'user' in session and session['user'].get('type') == 'recruiter':
            return redirect(url_for('admin.index'))
        return redirect(url_for('auth.login', type='recruiter'))

    @app.route("/api/check-session", methods=["GET"])
    def check_session():
        if 'user' in session:
            app.logger.info(f"Session data in check-session: {session['user']['userinfo']['name']}")
            app.logger.info(f"Session Type in check-session: {session['user']['type']}")
            return jsonify(session['user'])
        else:
            app.logger.info("No user in session in check-session")
            return jsonify({})
        
    @app.route('/uploads/<path:filename>')
    def serve_uploaded_file(filename):
        return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
    @app.before_request
    def before_request():
        app.logger.debug(f"Received request: {request.method} {request.path}")
        app.logger.info(f"Request method: {request.method}")
        # app.logger.info(f"Session before request: {session}")

    @app.after_request
    def after_request(response):
        # app.logger.info(f"Session after request: {session}")
        return response

    @app.errorhandler(RedisError)
    def handle_redis_error(error):
        app.logger.error(f"Redis error encountered: {error}")
        return "A problem occurred with our Redis service. Please try again later.", 500

    @app.route('/', defaults={'path': ''})
    @app.route('/<path:path>')
    def catch_all(path):
        app.logger.debug(f"Catch-all route hit: {path}")
        return f"You accessed path: {path}"
    
    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

