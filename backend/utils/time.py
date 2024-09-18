from datetime import datetime, timedelta
import time
from functools import wraps
from flask import current_app

def get_relative_time(date_str):
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    delta = today - date

    if delta.days <= 0:
        return 'Today'
    elif delta.days == 1:
        return '1d ago'
    elif delta.days < 7:
        return f'{delta.days}d ago'
    elif delta.days < 14:
        return '1w ago'
    elif delta.days < 21:
        return '2w ago'
    elif delta.days < 28:
        return '3w ago'
    elif delta.days < 31:
        return '4w ago'
    elif delta.days < 62:
        return '1m ago'
    else:
        return f'{delta.days // 30} months ago'
    
def timing_decorator(f):
    @wraps(f)
    def wrap(*args, **kw):
        ts = time.time()
        result = f(*args, **kw)
        te = time.time()
        current_app.logger.info(f'func:{f.__name__} took: {te-ts:2.4f} sec')
        return result
    return wrap