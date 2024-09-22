#!/bin/sh

set -e

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Run database migrations
echo "Running database migrations..."
if [ ! -d "migrations" ]; then
    echo "Migrations directory not found. Initializing..."
    flask db init
fi
flask db current || echo "No current revision"
flask db stamp head || echo "Failed to stamp head"
flask db migrate -m "initial migration" || echo "Failed to create migration"
flask db upgrade || {
    echo "Migration failed. Attempting to recreate migrations..."
    rm -rf migrations
    flask db init
    flask db stamp head
    flask db migrate -m "initial migration"
    flask db upgrade || { echo "Migration recreation failed"; exit 1; }
}

echo "Migrations completed."

# Add a small delay after migrations
echo "Waiting 5 seconds for database operations to complete..."
sleep 5

# Start the application
echo "Starting the application..."
exec gunicorn --config gunicorn_config.py "app:create_app()"