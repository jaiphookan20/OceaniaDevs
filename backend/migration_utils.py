import logging
import shutil
from sqlalchemy import text
from flask import current_app

logger = logging.getLogger(__name__)

def check_migration_safety():
    """Check if it's safe to run migrations."""
    try:
        engine = current_app.extensions['migrate'].db.engine
        with engine.connect() as connection:
            # Check for active transactions
            result = connection.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active' AND pid != pg_backend_pid()")).scalar()
            if result > 0:
                logger.warning(f"There are {result} active transactions. Migration might interfere with ongoing operations.")
                return False
            
            # Check available disk space (example for Unix systems)
            total, used, free = shutil.disk_usage("/")
            free_gb = free // (2**30)
            if free_gb < 5:  # Less than 5GB free
                logger.warning(f"Low disk space: only {free_gb}GB available. Migration might fail.")
                return False
            
            # Check database connection
            connection.execute(text("SELECT 1"))
            
            # Check if any tables are locked
            locked_tables = connection.execute(text("SELECT relation::regclass::text FROM pg_locks WHERE mode = 'AccessExclusiveLock' AND relation IS NOT NULL")).fetchall()
            if locked_tables:
                logger.warning(f"The following tables are locked: {', '.join([t[0] for t in locked_tables])}")
                return False

        return True
    except Exception as e:
        logger.error(f"Error during migration safety check: {e}")
        return False