from celery import Celery
from celery.schedules import crontab
import os
from dotenv import load_dotenv

load_dotenv()

# Create the Celery instance directly
app = Celery('job_board',
             broker=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
             include=['scrapers.ats_scraper', 'scrapers.seek_scraper'])

# Configure Celery
app.conf.update(
    broker_url=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
    result_backend=f"redis://{os.getenv('REDIS_HOST', 'redis')}:{os.getenv('REDIS_PORT', '6379')}/0",
    timezone='UTC',
    
    # Memory optimization settings
    worker_max_memory_per_child=100000,
    worker_max_tasks_per_child=10,
    task_time_limit=1800,
    worker_prefetch_multiplier=1,
    task_ignore_result=True,
    worker_concurrency=1,
)

# Configure the beat schedule
app.conf.beat_schedule = {
    'run-ats-scraper-daily': {
        'task': 'scrapers.ats_scraper.run_scheduled_scraper',
        'schedule': crontab(hour=21, minute=24),
    },
    'run-seek-scraper-daily': {
        'task': 'scrapers.seek_scraper.run_scheduled_scraper',
        'schedule': crontab(hour=12, minute=0),
    }
}