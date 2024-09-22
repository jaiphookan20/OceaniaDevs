from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from extensions import bcrypt, db
from models import Seeker, Recruiter
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from configparser import ConfigParser
from flask_cors import CORS
import config
import secrets
from datetime import timedelta

auth_blueprint = Blueprint('auth', __name__)
CORS(auth_blueprint, supports_credentials=True, resources={r"/*": {"origins": "*"}})
webapp_secret_key = config.AUTH0_SECRET_KEY
oauth = OAuth()

def generate_state():
    return secrets.token_urlsafe(32)

@auth_blueprint.before_request
def before_request():
    # current_app.logger.info(f"Session before request: {session}")
    current_app.logger.info(f"Request path: {request.path}")
    current_app.logger.info(f"Request method: {request.method}")

@auth_blueprint.after_request
def after_request(response):
    # current_app.logger.info(f"Session after request: {session}")
    return response

@auth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    try:
        current_app.logger.info("Callback initiated")
        current_app.logger.info(f"Request args: {request.args}")
        current_app.logger.info(f"Session before token: {session}")
        current_app.logger.info(f"Auth0 Domain: {config.AUTH0_DOMAIN}")
        current_app.logger.info(f"Auth0 Client ID: {config.AUTH0_CLIENT_ID}")
        current_app.logger.info(f"Callback URL: {url_for('auth.callback', _external=True)}")
        
        current_app.logger.info(f"Session state: {session.get('oauth_state')}")
        current_app.logger.info(f"Request state: {request.args.get('state')}")
        
        if session.get('oauth_state') != request.args.get('state'):
            raise ValueError("State mismatch. Possible CSRF attack.")
        
        token = oauth.auth0.authorize_access_token()
        
        current_app.logger.info("Token obtained successfully")
        current_app.logger.info(f"Session after token: {session}")

        session["user"] = token

        email = session.get('user').get('userinfo').get('email')
        registration_type = request.args.get('type')

        if registration_type == 'recruiter':
            existing_recruiter = Recruiter.query.filter_by(email=email).first()
            current_app.logger.info("Existing Recruiter Logged In" if existing_recruiter else "New Recruiter Created")
            if not existing_recruiter:
                new_recruiter = Recruiter(email=email)
                db.session.add(new_recruiter)
                db.session.commit()
            
            recruiter = Recruiter.query.filter_by(email=email).first()
            recruiter_id = recruiter.recruiter_id
            current_app.logger.info(f"Recruiter ID: {recruiter_id}")

            session["user"]["type"] = "recruiter"
            session["user"]["recruiter_id"] = recruiter_id
        else:
            existing_seeker = Seeker.query.filter_by(email=email).first()
            current_app.logger.info("Existing Seeker Logged In" if existing_seeker else "New Seeker Created")
            if not existing_seeker:
                new_seeker = Seeker(email=email)
                db.session.add(new_seeker)
                db.session.commit()
            
            seeker = Seeker.query.filter_by(email=email).first()
            uid = seeker.uid
            current_app.logger.info(f"Seeker ID: {uid}")
            
            session["user"]["type"] = "seeker"
            session["user"]["uid"] = uid

        current_app.logger.info(f"Session data after login: {session}")
        
        if session["user"]["type"] == "recruiter":
            if existing_recruiter:
                return redirect(f"{config.BASE_URL}")        
            else:
                return redirect(f"{config.BASE_URL}/employer/add-details")
        else:
            return redirect(f"{config.BASE_URL}")
    except Exception as e:
        current_app.logger.error(f"Error in callback: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@auth_blueprint.route("/login/<string:type>")
def login(type):
    try:
        state = generate_state()
        session['oauth_state'] = state
        current_app.logger.info(f"Generated state for login: {state}")
        current_app.logger.info(f"Session after setting state: {session}")
        current_app.logger.info(f"Auth0 Domain: {config.AUTH0_DOMAIN}")
        current_app.logger.info(f"Auth0 Client ID: {config.AUTH0_CLIENT_ID}")
        redirect_uri = url_for("auth.callback", _external=True) + f'?type={type}'
        current_app.logger.info(f"Redirect URI: {redirect_uri}")
        
        auth_url = oauth.auth0.authorize_redirect(
            redirect_uri=redirect_uri,
            state=state
        )
        current_app.logger.info(f"Generated Auth URL: {auth_url}")
        return auth_url
    except Exception as e:
        current_app.logger.error(f"Error in login route: {str(e)}", exc_info=True)
        return jsonify({"error": str(e)}), 500

@auth_blueprint.route("/register/<string:type>")
def signup(type):
    state = generate_state()
    session['oauth_state'] = state
    current_app.logger.info(f"Generated state for signup: {state}")
    current_app.logger.info(f"Session after setting state: {session}")
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
        state=state
    )

@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    session.clear()
    current_app.logger.info("User logged out, session cleared")
    return redirect(f"{config.BASE_URL}/")

# def init_auth(app):
#     oauth.init_app(app)
#     oauth.register(
#         "auth0",
#         client_id=config.AUTH0_CLIENT_ID,
#         client_secret=config.AUTH0_CLIENT_SECRET,
#         client_kwargs={
#             "scope": "openid profile email",
#         },
#         server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration'
#     )

def init_auth(app):
    print(f"Initializing Auth0 with domain: {config.AUTH0_DOMAIN}")
    oauth.init_app(app)
    oauth.register(
        "auth0",
        client_id=config.AUTH0_CLIENT_ID,
        client_secret=config.AUTH0_CLIENT_SECRET,
        client_kwargs={
            "scope": "openid profile email",
        },
        server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration'
    )
    print("Auth0 initialization completed")
    # print(f"Registered client: {oauth.auth0.__dict__}")