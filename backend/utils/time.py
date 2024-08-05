from datetime import datetime, timedelta

def get_relative_time(date_str):
    today = datetime.now().date()
    date = datetime.strptime(date_str, '%Y-%m-%d').date()
    delta = today - date

    if delta.days <= 0:
        return 'Today'
    elif delta.days == 1:
        return '1 day'
    elif delta.days < 7:
        return f'{delta.days} days ago'
    elif delta.days < 14:
        return '1 week'
    elif delta.days < 21:
        return '2 weeks'
    elif delta.days < 28:
        return '3 weeks'
    elif delta.days < 31:
        return '4 weeks'
    elif delta.days < 62:
        return '1 month'
    else:
        return f'{delta.days // 30} months ago'