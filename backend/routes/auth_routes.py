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

# @auth_blueprint.route("/login/<string:type>")
# def login(type):
#     state = generate_state()
#     session['oauth_state'] = state
#     current_app.logger.info(f"Generated state for login: {state}")
#     current_app.logger.info(f"Session after setting state: {session}")
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
#         state=state
#     )

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
    current_app.logger.info(f"Initializing Auth0 with domain: {config.AUTH0_DOMAIN}")
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
    current_app.logger.info("Auth0 initialization completed")
    current_app.logger.info(f"Registered client: {oauth.auth0.__dict__}")

    app.config['SESSION_TYPE'] = 'redis'
    app.config['SESSION_PERMANENT'] = True
    app.config['PERMANENT_SESSION_LIFETIME'] = timedelta(hours=1)
    app.config['SESSION_USE_SIGNER'] = True
    app.config['SESSION_COOKIE_SECURE'] = False  # Set to False since we're not using HTTPS
    app.config['SESSION_COOKIE_HTTPONLY'] = True
    app.config['SESSION_COOKIE_SAMESITE'] = 'Lax'

    return app


# THIS IS WORKING FINE. COMMENTED OUT TO TEST CODE ABOVE (MORE LOGGING TO DEBUG AUTH0 LOGIN ERROR)
# from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app, jsonify
# from extensions import bcrypt, db
# from models import Seeker, Recruiter
# from authlib.integrations.flask_client import OAuth
# from urllib.parse import quote_plus, urlencode
# from configparser import ConfigParser
# from flask_cors import CORS
# import config

# # Create a Blueprint for authentication routes
# auth_blueprint = Blueprint('auth', __name__)
# CORS(auth_blueprint, supports_credentials=True, resources={r"/*": {"origins": "*"}})

# # Access WEBAPP settings
# webapp_secret_key = config.AUTH0_SECRET_KEY

# # Initialize OAuth
# oauth = OAuth(current_app)
# oauth.register(
#     "auth0",
#     client_id=config.AUTH0_CLIENT_ID,
#     client_secret=config.AUTH0_CLIENT_SECRET,
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f'https://{config.AUTH0_DOMAIN}/.well-known/openid-configuration'
# )

# # Callback route for handling the redirect from Auth0 after authentication
# @auth_blueprint.route("/callback", methods=["GET", "POST"])
# def callback():
#     """
#     Callback route for handling the redirect from Auth0 after authentication.
#     This route is responsible for:
#     1. Obtaining the access token from Auth0
#     2. Storing the user information in the session
#     3. Checking if the user is a new or existing Seeker/Recruiter
#     4. Creating a new Seeker/Recruiter record if the user is new
#     5. Storing the user type and ID in the session
#     6. Redirecting the user to the React app homepage or recruiter signup page
#     """
#     try:
#         current_app.logger.info("Callback initiated")
#         current_app.logger.info(f"Request args: {request.args}")
#         current_app.logger.info(f"Session before token: {session}")
#         current_app.logger.info(f"Auth0 Domain: {config.AUTH0_DOMAIN}")
#         current_app.logger.info(f"Auth0 Client ID: {config.AUTH0_CLIENT_ID}")
#         current_app.logger.info(f"Callback URL: {url_for('auth.callback', _external=True)}")
        
#         token = oauth.auth0.authorize_access_token()
        
#         current_app.logger.info("Token obtained successfully")
#         current_app.logger.info(f"Session after token: {session}")

#         session["user"] = token

#         # Get the email from the user's session
#         email = session.get('user').get('userinfo').get('email')

#         # Check if the user came from the seeker or recruiter registration route
#         registration_type = request.args.get('type')

#         if registration_type == 'recruiter':
#             # Check if a Recruiter with the same email already exists
#             existing_recruiter = Recruiter.query.filter_by(email=email).first()
#             print("Existing Recruiter Logged In")
#             if not existing_recruiter:
#                 # If no Recruiter with the same email exists, create a new one
#                 print("New Recruiter Created")
#                 new_recruiter = Recruiter(email=email)
#                 db.session.add(new_recruiter)
#                 db.session.commit()
#         else:
#             # Check if a Seeker with the same email already exists
#             existing_seeker = Seeker.query.filter_by(email=email).first()
#             if not existing_seeker:
#                 # If no Seeker with the same email exists, create a new one
#                 print("New Seeker Created")
#                 new_seeker = Seeker(email=email)
#                 db.session.add(new_seeker)
#                 db.session.commit()

#         # If the user is registering as a recruiter
#         if registration_type == 'recruiter':
#             # Extract Email
#             recruiter = Recruiter.query.filter_by(email=email).first()
#             # Get the recruiter_id from the retrieved recruiter record
#             recruiter_id = recruiter.recruiter_id
#             print(f"Recruiter ID: {recruiter_id}")

#             # Store the user type as "recruiter" in the session
#             session["user"]["type"] = "recruiter"
#             # Store the recruiter_id in the session
#             session["user"]["recruiter_id"] = recruiter_id
#         else:
#             seeker = Seeker.query.filter_by(email=email).first()
#             uid = seeker.uid
#             print(f"Seeker ID: {seeker.uid}")
            
#             # Store the uid and type=seeker in the session object
#             session["user"]["type"] = "seeker"
#             session["user"]["uid"] = uid

#         print(f"Session data after login: {session}")
        
#         # Redirect to the React application homepage or recruiter signup page
#         if session["user"]["type"] == "recruiter":
#             if existing_recruiter:
#                 return redirect("http://localhost")        
#             else:
#                 return redirect("http://localhost/employer/add-details")
#         else:
#             return redirect("http://localhost")
#     except Exception as e:
#         current_app.logger.error(f"Error in callback: {str(e)}", exc_info=True)
#         return jsonify({"error": str(e)}), 500

# # Login Route:
# # @auth_blueprint.route("/login", defaults={'type': 'seeker'})
# @auth_blueprint.route("/login/<string:type>")
# def login(type):
#     """
#     Route for initiating the login process with Auth0.
#     Redirects the user to the Auth0 Universal Login page.
#     The 'type' parameter determines whether the user is a seeker or recruiter.
#     """
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
#         screen_hint="login"
#     )

# # Registration Route:
# # @auth_blueprint.route("/register", defaults={'type': 'seeker'})
# @auth_blueprint.route("/register/<string:type>")
# def signup(type):
#     """
#     Route for initiating the registration process with Auth0.
#     Redirects the user to the Auth0 Universal Login page.
#     The 'type' parameter determines whether the user is a seeker or recruiter.
#     """
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
#         screen_hint="signup"
#     )

# # Logout Route:
# @auth_blueprint.route("/logout", methods=["GET"])
# def logout():
#     """
#     Route for logging out the user from the application.
#     Clears the session and redirects the user to the home page.
#     """
#     session.clear()
#     return redirect("http://localhost/")