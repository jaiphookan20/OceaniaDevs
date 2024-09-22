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

# Use PGPASSWORD environment variable for psql
export PGPASSWORD=$DB_PASSWORD

flask db current || {
    echo "No current revision. Initializing database..."
    flask db stamp head
}
flask db migrate -m "initial migration" || echo "Failed to create migration"
flask db upgrade || {
    echo "Migration failed. Attempting to apply migrations without creating new ones..."
    flask db upgrade --sql | psql -U $DB_USER -d $DB_NAME -h $DB_HOST
    if [ $? -ne 0 ]; then
        echo "Migration recreation failed"
        exit 1
    fi
}

# Unset PGPASSWORD for security
unset PGPASSWORD

echo "Migrations completed."

# Add a small delay after migrations
echo "Waiting 5 seconds for database operations to complete..."
sleep 5

# Start the application
echo "Starting the application..."
exec gunicorn --config gunicorn_config.py "app:create_app()"