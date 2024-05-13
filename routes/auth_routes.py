from flask import Blueprint, render_template, request, redirect, url_for, session, flash, current_app
from extensions import bcrypt, db
from models import Seeker, Recruiter
from authlib.integrations.flask_client import OAuth
from urllib.parse import quote_plus, urlencode


from configparser import ConfigParser

auth_blueprint = Blueprint('auth', __name__)

# Initialize the ConfigParser
config_parser = ConfigParser()

# Read the configuration from the .config file
config_parser.read('.config')

# Access AUTH0 settings
auth0_client_id = config_parser.get('AUTH0', 'CLIENT_ID')
auth0_client_secret = config_parser.get('AUTH0', 'CLIENT_SECRET')
auth0_domain = config_parser.get('AUTH0', 'DOMAIN')


# Access WEBAPP settings
webapp_secret_key = config_parser.get('WEBAPP', 'SECRET_KEY')

# Initialize OAuth
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

# @auth_blueprint.route("/callback", methods=["GET", "POST"])
# def callback():
#     """
#     Callback redirect from Auth0
#     """
#     token = oauth.auth0.authorize_access_token()
#     session["user"] = token

#     """ Get the email from the user's session """
#     email = session.get('user').get('userinfo').get('email')

#     """ Check if a Seeker with the same email already exists """
#     existing_seeker = Seeker.query.filter_by(email=email).first()
    
#     if not existing_seeker:
#         """ If no Seeker with the same email exists, create a new one """
#         new_seeker = Seeker(email=email)
#         db.session.add(new_seeker)
#         db.session.commit()

#     seeker = existing_seeker or Seeker.query.filter_by(email=email).first()
#     uid = seeker.uid
#     # Store the uid in the session object
#     session["user"]["uid"] = uid

#     return redirect(url_for('home'))

@auth_blueprint.route("/callback", methods=["GET", "POST"])
def callback():
    """
    Callback redirect from Auth0
    """
    token = oauth.auth0.authorize_access_token()
    session["user"] = token

    """ Get the email from the user's session """
    email = session.get('user').get('userinfo').get('email')

    # Check if the user came from the seeker or recruiter registration route
    registration_type = request.args.get('type')

    if registration_type == 'recruiter':
        """ Check if a Recruiter with the same email already exists """
        existing_recruiter = Recruiter.query.filter_by(email=email).first()
        print("Existing Recruiter Logged In")
        if not existing_recruiter:
            """ If no Recruiter with the same email exists, create a new one """
            print("New Recruiter Created")
            new_recruiter = Recruiter(email=email)
            db.session.add(new_recruiter)
            db.session.commit()
    else:
        """ Check if a Seeker with the same email already exists """
        existing_seeker = Seeker.query.filter_by(email=email).first()
        print("Existing Seeker Logged In")
        if not existing_seeker:
            """ If no Seeker with the same email exists, create a new one """
            print("New Seeker Created")
            new_seeker = Seeker(email=email)
            db.session.add(new_seeker)
            db.session.commit()

    # user = Recruiter.query.filter_by(email=email).first() if registration_type == 'recruiter' else Seeker.query.filter_by(email=email).first()
    # uid = user.uid

    if registration_type == 'recruiter':
        recruiter = Recruiter.query.filter_by(email=email).first()
        recruiter_id = recruiter.recruiter_id
        print(f"Recruiter ID: {recruiter_id}")
        session["user"]["type"] = "recruiter"
        session["user"]["recruiter_id"] = recruiter_id
    else:
        seeker = Seeker.query.filter_by(email=email).first()
        uid=seeker.uid
        print(f"Seeker ID: ${seeker.uid}")
        # Store the uid and type=seeker in the session object
        session["user"]["type"] = "seeker"
        session["user"]["uid"] = uid
    
    return redirect(url_for('home'))


# @auth_blueprint.route("/login")
# def login():
#     """
#     Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
#     """
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("auth.callback", _external=True)
#     )

# @auth_blueprint.route("/register")
# def signup():
#     """
#     Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
#     """
#     return oauth.auth0.authorize_redirect(
#         redirect_uri=url_for("auth.callback", _external=True),
#         screen_hint="signup"
#     )

@auth_blueprint.route("/login", defaults={'type': 'seeker'})
@auth_blueprint.route("/login/<string:type>")
def login(type):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
        screen_hint="login"
    )

@auth_blueprint.route("/register", defaults={'type': 'seeker'})
@auth_blueprint.route("/register/<string:type>")
def signup(type):
    """
    Redirects the user to the Auth0 Universal Login (https://auth0.com/docs/authenticate/login/auth0-universal-login)
    """
    return oauth.auth0.authorize_redirect(
        redirect_uri=url_for("auth.callback", _external=True) + f'?type={type}',
        screen_hint="signup"
    )

@auth_blueprint.route("/logout")
def logout():
    """
    Logs the user out of the session and from the Auth0 tenant
    """
    session.clear()
    return redirect(url_for('home'))