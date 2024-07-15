#!/bin/sh

echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

flask db upgrade

if [ "$FLASK_ENV" = "development" ]; then
    echo "Starting Flask development server with hot reloading..."
    python -m flask run --host=0.0.0.0 --port=4040 --reload
else
    echo "Starting Gunicorn production server..."
    gunicorn --config gunicorn_config.py "app:create_app()"
fi

# #!/bin/sh

# # Wait for the database to be ready
# echo "Waiting for PostgreSQL..."
# while ! nc -z $DB_HOST 5432; do
#   sleep 1
# done
# echo "PostgreSQL started"

# # Run migrations
# flask db upgrade

# # Start the application
# gunicorn --bind 0.0.0.0:4040 "app:create_app()"