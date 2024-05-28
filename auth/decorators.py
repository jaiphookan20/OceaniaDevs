from flask import redirect, session, url_for
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
            print('Unauthorized 2: Need to login first')
            print(url_for('home'))
            return redirect(url_for('home'))

        return f(*args, **kwargs)

    return decorated