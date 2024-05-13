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
    return render_template('index.html', user_logged_in=user_logged_in)

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