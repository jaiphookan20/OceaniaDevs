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
        timezone='UTC',
        
        # Memory optimization settings
        worker_max_memory_per_child=100000,  # 100MB memory limit
        worker_max_tasks_per_child=10,       # Restart worker frequently
        task_time_limit=1800,                # 30 min timeout
        worker_prefetch_multiplier=1,        # Don't prefetch tasks
        task_ignore_result=True,             # Don't store task results
        
        # Reduced task concurrency
        worker_concurrency=1,
    )

    # Spread out the schedule to avoid concurrent runs
    celery.conf.beat_schedule = {
        'run-ats-scraper-daily': {
            'task': 'scrapers.ats_scraper.run_scheduled_scraper',
            'schedule': crontab(hour=20, minute=55),  # Early morning
        },
        'run-seek-scraper-daily': {
            'task': 'scrapers.seek_scraper.run_scheduled_scraper',
            'schedule': crontab(hour=12, minute=0),  # Noon
        }
    }

    return celery