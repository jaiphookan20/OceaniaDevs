import subprocess
import logging
import os
from flask import current_app
from flask.cli import ScriptInfo
from sqlalchemy import text
from extensions import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def run_safety_checks():
    script_info = ScriptInfo()
    app = script_info.load_app()
    with app.app_context():
        result = app.test_cli_runner().invoke(app.cli.commands['check_safety'])
    return "Migration safety check passed." in result.output

def apply_custom_migration():
    try:
        with open('postgres/init-pgvector.sql', 'r') as file:
            sql = file.read()
        with current_app.app_context():
            db.session.execute(text(sql))
            db.session.commit()
        return True
    except Exception as e:
        logger.error(f"Custom migration failed: {e}")
        return False

def apply_migration():
    try:
        subprocess.run(["flask", "db", "upgrade"], check=True)
        return True
    except subprocess.CalledProcessError as e:
        logger.error(f"Migration failed: {e}")
        return False

def main():
    logger.info("Starting migration process")
    
    if not run_safety_checks():
        logger.error("Safety checks failed. Aborting migration.")
        return

    if apply_custom_migration():
        logger.info("Custom migration completed successfully")
    else:
        logger.warning("Custom migration failed.")

    if apply_migration():
        logger.info("Standard migration completed successfully")
    else:
        logger.warning("Standard migration failed.")

if __name__ == "__main__":
    main()