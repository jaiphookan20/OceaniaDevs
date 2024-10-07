#!/bin/sh

set -e

echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

if [ "$FLASK_ENV" = "production" ]; then
  echo "Running production migration process..."
  python migration_orchestrator.py
else
  echo "Running development migration process..."
  flask db upgrade
fi

# Start the application
echo "Starting the application..."
exec gunicorn --config gunicorn_config.py "app:create_app()"