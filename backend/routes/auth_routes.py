from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
from extensions import bcrypt, db
from models import Seeker, Recruiter
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode
from configparser import ConfigParser
from flask_cors import CORS

auth_blueprint = Blueprint('auth', __name__)
CORS(auth_blueprint, supports_credentials=True, resources={r"/*": {"origins": "http://localhost"}})

config_parser = ConfigParser()
config_parser.read('.config')

auth0_client_id = config_parser.get('AUTH0', 'CLIENT_ID')
auth0_client_secret = config_parser.get('AUTH0', 'CLIENT_SECRET')
auth0_domain = config_parser.get('AUTH0', 'DOMAIN')

webapp_secret_key = config_parser.get('WEBAPP', 'SECRET_KEY')

oauth = OAuth(current_app)
oauth.register(
    "auth0",
    client_id=auth0_client_id,
    client_secret=auth0_client_secret,
    client_kwargs={
        "scope": "openid profile email",
    },
    server_metadata_url=f'https://{auth0_domain}/.well-known/openid-configuration'
)

@auth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback route for handling the redirect from Auth0 after authentication.
    This route is responsible for:
    1. Obtaining the access token from Auth0
    2. Storing the user information in the session
    3. Checking if the user is a new or existing Seeker/Recruiter
    4. Creating a new Seeker/Recruiter record if the user is new
    5. Storing the user type and ID in the session
    6. Redirecting the user to the React app homepage or recruiter signup page
    """
    try:
        token = oauth.auth0.authorize_access_token()
        session["user"] = token
        
        # Get the email from the user's session
        email = session.get('user', {}).get('userinfo', {}).get('email')
        if not email:
            current_app.logger.error("No email found in user info")
            return jsonify({"error": "No email found"}), 400

        # Check if the user came from the seeker or recruiter registration route
        registration_type = request.args.get('type')
        current_app.logger.info(f"Registration type: {registration_type}")
        
        if registration_type == 'recruiter':
            # Check if a Recruiter with the same email already exists
            existing_recruiter = Recruiter.query.filter_by(email=email).first()
            current_app.logger.info("Existing Recruiter Logged In" if existing_recruiter else "New Recruiter Created")
            
            if not existing_recruiter:
                # If no Recruiter with the same email exists, create a new one
                new_recruiter = Recruiter(email=email)
                db.session.add(new_recruiter)
                db.session.commit()
            
            recruiter = existing_recruiter or new_recruiter
            recruiter_id = recruiter.recruiter_id
            current_app.logger.info(f"Recruiter ID: {recruiter_id}")
            
            # Store the user type and recruiter_id in the session
            session["user"].update({
                "type": "recruiter",
                "recruiter_id": recruiter_id
            })
        else:
            # Check if a Seeker with the same email already exists
            existing_seeker = Seeker.query.filter_by(email=email).first()
            current_app.logger.info("Existing Seeker Logged In" if existing_seeker else "New Seeker Created")
            
            if not existing_seeker:
                # If no Seeker with the same email exists, create a new one
                new_seeker = Seeker(email=email)
                db.session.add(new_seeker)
                db.session.commit()
            
            seeker = existing_seeker or new_seeker
            uid = seeker.uid
            current_app.logger.info(f"Seeker ID: {uid}")
            
            # Store the uid and type=seeker in the session object
            session["user"].update({
                "type": "seeker",
                "uid": uid
            })

        current_app.logger.info(f"Final session state: {session}")
        
        # Redirect to the React application homepage or recruiter signup page
        if session["user"]["type"] == "recruiter":
            if existing_recruiter:
                return redirect("http://localhost/")        
            else:
                return redirect("http://localhost/register/employer/info")
        else:
            return redirect("http://localhost/")

    except Exception as e:
        current_app.logger.error(f"Error in callback: {str(e)}")
        return jsonify({"error": str(e)}), 500

@auth_blueprint.route("/login/<string:type>")
def login(type):
    current_app.logger.info('User authenticated. Session: %s', session)
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True, _scheme='http') + f'?type={type}',
        screen_hint="login"
    )

@auth_blueprint.route("/register/<string:type>")
def signup(type):
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True, _scheme='http') + f'?type={type}',
        screen_hint="signup"
    )

@auth_blueprint.route("/logout", methods=["GET"])
def logout():
    current_app.logger.info('Logout. Session before clear: %s', session)
    session.clear()
    return redirect("http://localhost")
