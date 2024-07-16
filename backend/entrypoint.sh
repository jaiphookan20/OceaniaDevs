# Main fix (trying to replace the file inside lightsail)
#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Run migrations
flask db upgrade

# Start the application
gunicorn --bind 0.0.0.0:4040 "app:create_app()"