#!/bin/sh

set -e

if [ "$FLASK_ENV" = "production" ]; then
  DB_HOST=$LIGHTSAIL_DB_HOST
elif [ "$FLASK_ENV" = "staging" ]; then
  DB_HOST=$STAGING_DB_HOST
else
  DB_HOST=$DB_HOST
fi

echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

if [ "$FLASK_ENV" = "production" ]; then
  DB_HOST=$LIGHTSAIL_DB_HOST
elif [ "$FLASK_ENV" = "staging" ]; then
  DB_HOST=$STAGING_DB_HOST
else
  DB_HOST=${DB_HOST:-postgres}
fi

# Start the application
echo "Starting the application..."
exec gunicorn --config gunicorn_config.py "app:create_app()"