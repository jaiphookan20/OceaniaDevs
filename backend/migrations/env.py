import logging
from logging.config import fileConfig
import sys
import time
from sqlalchemy import text
from flask import current_app
from alembic import context

# this is the Alembic Config object, which provides
# access to the values within the .ini file in use.
config = context.config

# Interpret the config file for Python logging.
# This line sets up loggers basically.
fileConfig(config.config_file_name)
logger = logging.getLogger('alembic.env')


def get_engine():
    try:
        # this works with Flask-SQLAlchemy<3 and Alchemical
        return current_app.extensions['migrate'].db.get_engine()
    except (TypeError, AttributeError):
        # this works with Flask-SQLAlchemy>=3
        return current_app.extensions['migrate'].db.engine


def get_engine_url():
    try:
        return get_engine().url.render_as_string(hide_password=False).replace(
            '%', '%%')
    except AttributeError:
        return str(get_engine().url).replace('%', '%%')


# add your model's MetaData object here
# for 'autogenerate' support
# from myapp import mymodel
# target_metadata = mymodel.Base.metadata
config.set_main_option('sqlalchemy.url', get_engine_url())
target_db = current_app.extensions['migrate'].db

# other values from the config, defined by the needs of env.py,
# can be acquired:
# my_important_option = config.get_main_option("my_important_option")
# ... etc.


def get_metadata():
    if hasattr(target_db, 'metadatas'):
        return target_db.metadatas[None]
    return target_db.metadata


def run_migrations_offline():
    """Run migrations in 'offline' mode.

    This configures the context with just a URL
    and not an Engine, though an Engine is acceptable
    here as well.  By skipping the Engine creation
    we don't even need a DBAPI to be available.

    Calls to context.execute() here emit the given string to the
    script output.

    """
    url = config.get_main_option("sqlalchemy.url")
    context.configure(
        url=url, target_metadata=get_metadata(), literal_binds=True
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Run migrations in 'online' mode."""
    try:
        connectable = get_engine()
        with connectable.connect() as connection:
            context.configure(
                connection=connection,
                target_metadata=get_metadata(),
                **current_app.extensions['migrate'].configure_args
            )

            with context.begin_transaction():
                context.run_migrations()
    except Exception as e:
        logger.error(f"Error during migration: {e}")
        raise

def check_migration_safety():
    """Check if it's safe to run migrations."""
    try:
        engine = get_engine()
        with engine.connect() as connection:
            # Check for active transactions
            result = connection.execute(text("SELECT count(*) FROM pg_stat_activity WHERE state = 'active' AND pid != pg_backend_pid()")).scalar()
            if result > 0:
                logger.warning(f"There are {result} active transactions. Migration might interfere with ongoing operations.")
                return False

        return True
    except Exception as e:
        logger.error(f"Error during migration safety check: {e}")
        return False

        return True
    except Exception as e:
        logger.error(f"Error during migration safety check: {e}")
        return False

# Call this function before running migrations
if not check_migration_safety():
    logger.error("Migration safety check failed. Aborting.")
    sys.exit(1)


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

# Add a small delay after migrations
time.sleep(5)
logger.info("Waiting 5 seconds for database operations to complete...")
