from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

def create_celery_app(app=None):
    celery = Celery('job_board',
                    broker=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
                    include=['scrapers.ats_scraper', 'scrapers.seek_scraper'])
    
    celery.conf.update(
        broker_url=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
        result_backend=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
        timezone='UTC'
    )

    # Configure periodic tasks
    celery.conf.beat_schedule = {
        'run-ats-scraper-daily': {
            'task': 'tasks.run_ats_scraper',
            'schedule': crontab(hour=0, minute=0),  # Run at midnight every day
        },
        'run-seek-scraper-daily': {
            'task': 'tasks.run_seek_scraper',
            'schedule': crontab(hour=12, minute=0),  # Run at noon every day
        }
    }

    return celery