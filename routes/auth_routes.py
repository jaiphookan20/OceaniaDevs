from flask import Blueprint, request, session, jsonify, redirect
from extensions import db
from models import Seeker, Recruiter
from flask_cors import CORS
from supabase import create_client
from flask import Blueprint, request, jsonify, session as flask_session
from jwt.exceptions import ExpiredSignatureError, InvalidTokenError

auth_blueprint = Blueprint('auth', __name__)
CORS(auth_blueprint)

supabase = create_client("https://uyrnqtinwxwhtlaswyrf.supabase.co", "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJzdXBhYmFzZSIsInJlZiI6InV5cm5xdGlud3h3aHRsYXN3eXJmIiwicm9sZSI6ImFub24iLCJpYXQiOjE3MTg1NTQwMzcsImV4cCI6MjAzNDEzMDAzN30.IJjZWNKGU_fPofRw-LDYybPUsCaUZwUJSZ3gXSejwNM")

# auth_routes.py
import jwt

auth_blueprint = Blueprint('auth', __name__)
JWT_SECRET = "zg5afH0tHafxcWgYvPBxZ0DCSqQs5w/jHziIxHsTZFgGqBWzsGDZ17NUA4gT3fFzTL5vuq9IUGTltpZ4uMuo3g=="

@auth_blueprint.route("/callback", methods=["POST"])
def callback():
    auth_header = request.headers.get('Authorization', None)
    # print(f"auth_header: {auth_header}")
    # session_data = request.json.get('session')
    # print(f"session: {session_data}")
    if not auth_header:
        return jsonify({'error': 'Authorization header is missing'}), 400

    try:
        # Extract token from header
        token = auth_header.split(" ")[1]
        # Decode the JWT without verifying the audience yet
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], options={"verify_aud": False})
        # print(f"decoded_token: {decoded_token}")

        # Extract audience from the token
        expected_audience = decoded_token['aud']

        # Decode the JWT with audience check
        decoded_token = jwt.decode(token, JWT_SECRET, algorithms=["HS256"], audience=expected_audience)
        # print(f"decoded_token with audience verification: {decoded_token}")

        user_id = decoded_token['sub']
        user_email = decoded_token['email']
        user_name = decoded_token.get('name')

        # Store user information in the session
        session['user'] = {
            # 'id': user_id,
            'email': user_email,
            'name': user_name,
        }
        # print(session['user'])
        return redirect("http://localhost:3000/")

    except ExpiredSignatureError:
        return jsonify({'error': 'Token has expired'}), 401
    except InvalidTokenError as e:
        print(f"Invalid token: {e}")
        return jsonify({'error': 'Invalid token'}), 401

@auth_blueprint.route("/logout")
def logout():
    session.clear()
    return jsonify({'success': True}), 200
# @auth_blueprint.route("/callback", methods=["POST"])
# def callback():
#     data = request.json
#     user_id = data.get('id')
#     email = data.get('email')
#     name = data.get('name')
#     registration_type = data.get('type')
#     print('Inside callback');
#     print(data)

#     if not user_id or not email or not name:
#         return jsonify({"error": "Invalid data"}), 400

#     if registration_type == 'recruiter':
#         existing_recruiter = Recruiter.query.filter_by(email=email).first()
#         if not existing_recruiter:
#             new_recruiter = Recruiter(email=email)
#             db.session.add(new_recruiter)
#             db.session.commit()
#     else:
#         existing_seeker = Seeker.query.filter_by(email=email).first()
#         if not existing_seeker:
#             new_seeker = Seeker(email=email)
#             db.session.add(new_seeker)
#             db.session.commit()

#     if registration_type == 'recruiter':
#         recruiter = Recruiter.query.filter_by(email=email).first()
#         recruiter_id = recruiter.recruiter_id
#         session["user"] = {
#             "id": user_id,
#             "name": name,
#             "email": email,
#             "type": "recruiter",
#             "recruiter_id": recruiter_id
#         }
#     else:
#         seeker = Seeker.query.filter_by(email=email).first()
#         uid = seeker.uid
#         session["user"] = {
#             "id": user_id,
#             "name": name,
#             "email": email,
#             "type": "seeker",
#             "uid": uid
#         }

#     return jsonify({"message": "User data received and session created successfully"}), 200





# from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
# from extensions import bcrypt, db
# from models import Seeker, Recruiter
# from authlib.integrations.flask_client import OAuth
# from urllib.parse import quote_plus, urlencode
# from configparser import ConfigParser
# from flask_cors import CORS

# # Create a Blueprint for authentication routes
# auth_blueprint = Blueprint('auth', __name__)
# CORS(auth_blueprint)

# # Initialize the ConfigParser
# config_parser = ConfigParser()

# # Read the configuration from the .config file
# config_parser.read('.config')

# # Access AUTH0 settings
# auth0_client_id = config_parser.get('AUTH0', 'CLIENT_ID')
# auth0_client_secret = config_parser.get('AUTH0', 'CLIENT_SECRET')
# auth0_domain = config_parser.get('AUTH0', 'DOMAIN')

# # Access WEBAPP settings
# webapp_secret_key = config_parser.get('WEBAPP', 'SECRET_KEY')

# # Initialize OAuth
# oauth = OAuth(current_app)
# oauth.register(
#     "auth0",
#     client_id=auth0_client_id,
#     client_secret=auth0_client_secret,
#     client_kwargs={
#         "scope": "openid profile email",
#     },
#     server_metadata_url=f'https://{auth0_domain}/.well-known/openid-configuration'
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
#     6. Redirecting the user to the React app homepage
#     """
#     token = oauth.auth0.authorize_access_token()
#     session["user"] = token

#     # Get the email from the user's session
#     email = session.get('user').get('userinfo').get('email')

#     # Check if the user came from the seeker or recruiter registration route
#     registration_type = request.args.get('type')

#     if registration_type == 'recruiter':
#         # Check if a Recruiter with the same email already exists
#         existing_recruiter = Recruiter.query.filter_by(email=email).first()
#         print("Existing Recruiter Logged In")
#         if not existing_recruiter:
#             # If no Recruiter with the same email exists, create a new one
#             print("New Recruiter Created")
#             new_recruiter = Recruiter(email=email)
#             db.session.add(new_recruiter)
#             db.session.commit()
#     else:
#         # Check if a Seeker with the same email already exists
#         existing_seeker = Seeker.query.filter_by(email=email).first()
#         if not existing_seeker:
#             # If no Seeker with the same email exists, create a new one
#             print("New Seeker Created")
#             new_seeker = Seeker(email=email)
#             db.session.add(new_seeker)
#             db.session.commit()

#     # If the user is registering as a recruiter
#     if registration_type == 'recruiter':
#         # Extract Email
#         recruiter = Recruiter.query.filter_by(email=email).first()
#         # Get the recruiter_id from the retrieved recruiter record
#         recruiter_id = recruiter.recruiter_id
#         print(f"Recruiter ID: {recruiter_id}")

#         # Store the user type as "recruiter" in the session
#         session["user"]["type"] = "recruiter"
#         # Store the recruiter_id in the session
#         session["user"]["recruiter_id"] = recruiter_id
#     else:
#         seeker = Seeker.query.filter_by(email=email).first()
#         uid = seeker.uid
#         print(f"Seeker ID: {seeker.uid}")
        
#         # Store the uid and type=seeker in the session object
#         session["user"]["type"] = "seeker"
#         session["user"]["uid"] = uid

#     print(f"Session data after login: {session}")
    
#     # Redirect to the React application homepage
#     return redirect("http://localhost:3000/")

# # Login Route:
# @auth_blueprint.route("/login", defaults={'type': 'seeker'})
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
# @auth_blueprint.route("/register", defaults={'type': 'seeker'})
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
# @auth_blueprint.route("/logout")
# def logout():
#     """
#     Route for logging out the user from the application.
#     Clears the session and redirects the user to the home page.
#     """
#     session.clear()
#     # From Auth0 logout - add in code to track/inform Auth0 of logout
#     return redirect("http://localhost:3000/")