#!/bin/sh

# Wait for the database to be ready
while ! pg_isready -h postgres -U jai -d job_board; do
  echo "Waiting for PostgreSQL..."
  sleep 1
done

# Additional wait to ensure the vector extension is created
sleep 5

# Run migrations (if you're using Alembic)
flask db upgrade

# Start the application
gunicorn --bind 0.0.0.0:4040 --config gunicorn_config.py "app:create_app()"

# #!/bin/sh

# # Wait for the database to be ready
# while ! nc -z $DB_HOST 5432; do
#   echo "Waiting for postgres..."
#   sleep 1
# done

# echo "PostgreSQL started"

# # Run database migrations
# alembic upgrade head

# # Start the application
# gunicorn --bind 0.0.0.0:4040 --config gunicorn_config.py "app:create_app()"
