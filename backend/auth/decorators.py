from flask import redirect, session, url_for, jsonify
from functools import wraps


class AuthError(Exception):
    def __init__(self, error, status_code):
        self.error = error
        self.status_code = status_code


def requires_auth(f):
    """
    Use on routes that require a valid session, otherwise it aborts with a 403
    """
    @wraps(f)
    def decorated(*args, **kwargs):
        if session.get('user') is None:
            return jsonify({"error": "Unauthorized", "login_required": True}), 401
        return f(*args, **kwargs)
        # if session.get('user') is None:
        #     print('Unauthorized: Need to login first')
        #     return redirect(url_for('auth.login', type='seeker')) # Need to fix this. Not redirecting to Auth0 login correctly
    return decorated