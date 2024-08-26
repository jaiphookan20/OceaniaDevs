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
from models import Job, Company, Recruiter, state_enum, country_enum, job_type_enum, industry_enum, salary_range_enum
from matching.custom_types import Vector

load_dotenv()

def create_app():
    app = Flask(__name__)
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

    @app.route('/')
    def home():
        user_logged_in = 'user' in session
        if user_logged_in:
            app.logger.info(f"User logged in: {session.get('user').get('userinfo').get('name')}")
            app.logger.info(f"User Type: {session['user']['type']}")
        else:
            app.logger.info("User not in session")
        return jsonify({"status": "API is running", "user_logged_in": user_logged_in})

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
        app.logger.info(f"Request path: {request.path}")
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

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(debug=True)

# THIS WAS WORKING CORRECTLY:
# from flask import Flask, jsonify, request, session, redirect, url_for, send_from_directory, current_app
# from flask_session import Session
# from redis import Redis, RedisError
# from routes.auth_routes import auth_blueprint
# from routes.job_routes import job_blueprint
# from routes.recruiter_routes import recruiter_blueprint
# from routes.seeker_routes import seeker_blueprint
# from matching.similarity_search_routes import simsearch_blueprint
# from extensions import db, bcrypt, migrate, cache
# from routes.auth_routes import webapp_secret_key
# import logging
# from flask_cors import CORS
# from dotenv import load_dotenv
# import os
# from flask_migrate import Migrate
# from models import Job, Company, Recruiter, state_enum, country_enum, job_type_enum, industry_enum, salary_range_enum
# from matching.custom_types import Vector

# load_dotenv()

# def create_app():
#     app = Flask(__name__)
#     CORS(app, supports_credentials=True, resources={r"/*": {"origins": "*"}})
#     app.config['CORS_HEADERS'] = 'Content-Type'

#     # Define the upload subdirectory
#     UPLOAD_FOLDER = os.path.join('uploads', 'upload_company_logo')
#     app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

#     # Make sure the entire directory structure exists
#     os.makedirs(UPLOAD_FOLDER, exist_ok=True)

#     # Database configuration
#     DB_HOST = os.environ.get('DB_HOST', 'localhost')
#     DB_NAME = os.environ.get('DB_NAME', 'job_board')
#     DB_USER = os.environ.get('DB_USER', 'jai')
#     DB_PASSWORD = os.environ.get('DB_PASSWORD', 'techboard')

#     # Redis configuration
#     REDIS_HOST = os.environ.get('REDIS_HOST', 'localhost')
#     REDIS_PORT = int(os.environ.get('REDIS_PORT', 6379))

#     # Use test database if in testing environment
#     if os.getenv("FLASK_ENV") == "testing":
#         print('Running Test DB')
#         app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}_test'
#     else:
#         app.config['SQLALCHEMY_DATABASE_URI'] = f'postgresql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}/{DB_NAME}'

#     app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
#     app.config.update(
#         SESSION_COOKIE_SECURE=True,
#         SESSION_COOKIE_HTTPONLY=True,
#         SESSION_COOKIE_SAMESITE='Lax',
#     )
#     app.logger.setLevel(logging.INFO)

#     # Initialize extensions with the app
#     db.init_app(app)
#     bcrypt.init_app(app)
#     migrate.init_app(app, db)

#     # Register ENUM types
#     def create_enums():
#         with app.app_context():
#             db.create_all()  # Create the tables after enums are created
#             print("Database tables created successfully.")
#             for enum in [state_enum, country_enum, job_type_enum, industry_enum, salary_range_enum]:
#                 enum.create(bind=db.engine, checkfirst=True)

#     create_enums()

#     # Register blueprints
#     app.register_blueprint(auth_blueprint)
#     app.register_blueprint(job_blueprint)
#     app.register_blueprint(recruiter_blueprint)
#     app.register_blueprint(seeker_blueprint)
#     app.register_blueprint(simsearch_blueprint)

#     # Flask-Session configuration
#     app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', webapp_secret_key)
#     app.config['SESSION_TYPE'] = 'redis'
#     app.config['SESSION_PERMANENT'] = True
#     app.config['SESSION_USE_SIGNER'] = True
#     app.config['SESSION_REDIS'] = Redis(host=REDIS_HOST, port=REDIS_PORT, db=0)
#     app.config['PERMANENT_SESSION_LIFETIME'] = 86400  # Sessions last for one day

#     # Redis Caching Configuration
#     app.config['CACHE_TYPE'] = 'RedisCache'
#     app.config['CACHE_REDIS_HOST'] = REDIS_HOST
#     app.config['CACHE_REDIS_PORT'] = REDIS_PORT
#     app.config['CACHE_REDIS_DB'] = 0
#     app.config['CACHE_REDIS_URL'] = f'redis://{REDIS_HOST}:{REDIS_PORT}/0'
#     app.config['CACHE_DEFAULT_TIMEOUT'] = 300

#     cache.init_app(app)  # Initialize the Cache instance with the app
#     Session(app)

#     @app.route('/')
#     def home():
#         # Check if a user is logged in
#         user_logged_in = 'user' in session
#         if user_logged_in:
#             print(session.get('user').get("userinfo").get('name'))
#             user_type = session['user']['type'] in session
#             print(f"User Type: {session['user']['type']}")
#             print("User in session")
#         else:
#             print("User not in session")
#         return jsonify({"status": "API is running", "user_logged_in": user_logged_in})

#     @app.route("/api/check-session", methods=["GET"])
#     def check_session():
#         if 'user' in session:
#             print(f"Session data in check-session: {session['user']['userinfo']['name']}")
#             print(f"Session Type in check-session: {session['user']['type']}")
#             return jsonify(session['user'])
#         else:
#             print("No user in session in check-session")
#             return jsonify({})
        
#     # Serve the uploaded files
#     @app.route('/uploads/<path:filename>')
#     def serve_uploaded_file(filename):
#         return send_from_directory(app.config['UPLOAD_FOLDER'], filename)
        
#     @app.before_request
#     def before_request():
#         headers = {'Access-Control-Allow-Origin': '*',
#                 'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
#                 'Access-Control-Allow-Headers': 'Content-Type'}
#         if request.method.lower() == 'options':
#             return jsonify(headers), 200

#     @app.errorhandler(RedisError)
#     def handle_redis_error(error):
#         app.logger.error(f"Redis error encountered: {error}")
#         return "A problem occurred with our Redis service. Please try again later.", 500

#     return app

# if __name__ == '__main__':
#     app = create_app()
#     app.run(debug=True)