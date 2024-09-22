#!/bin/sh

# echo "Printing all environment variables:"
# env

# echo "Specific checks for Auth0 variables:"
# echo "AUTH0_DOMAIN: $AUTH0_DOMAIN"
# echo "AUTH0_CLIENT_ID: $AUTH0_CLIENT_ID"
# echo "AUTH0_CLIENT_SECRET is set: $(if [ -n "$AUTH0_CLIENT_SECRET" ]; then echo "Yes"; else echo "No"; fi)"
# echo "APP_SECRET_KEY is set: $(if [ -n "$APP_SECRET_KEY" ]; then echo "Yes"; else echo "No"; fi)"

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Wait an additional 10 seconds for the init script to complete
sleep 10

# Run database migrations
echo "Running database migrations..."
flask db upgrade || { echo "Migration failed"; exit 1; }

echo "Migrations completed."

# Add a small delay after migrations
echo "Waiting 5 seconds for database operations to complete..."
sleep 5

# Start the application
echo "Starting the application..."
gunicorn --config gunicorn_config.py "app:create_app()"