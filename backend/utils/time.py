from datetime import datetime, timedelta

def get_relative_time(date_str):
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    delta = today - date

    if delta.days <= 0:
        return 'Today'
    elif delta.days == 1:
        return '1 day ago'
    elif delta.days < 7:
        return f'{delta.days} days ago'
    elif delta.days < 14:
        return '1 week ago'
    elif delta.days < 21:
        return '2 weeks ago'
    elif delta.days < 28:
        return '3 weeks ago'
    elif delta.days < 31:
        return '4 weeks ago'
    elif delta.days < 62:
        return '1 month ago'
    else:
        return f'{delta.days // 30} months ago'