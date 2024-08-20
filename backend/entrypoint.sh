#!/bin/sh

# Wait for the database to be ready
echo "Waiting for PostgreSQL..."
while ! nc -z $DB_HOST 5432; do
  sleep 1
done
echo "PostgreSQL started"

# Wait an additional 10 seconds for the init script to complete
sleep 10

# Ensure correct permissions for the app directory
chown -R www-data:www-data /app

# Run migrations with verbose output
echo "Running database migrations..."
su www-data -s /bin/sh -c "flask db upgrade --verbose"

# Check if migrations were successful
if [ $? -ne 0 ]; then
    echo "Migration failed. Exiting..."
    exit 1
fi

echo "Migrations completed successfully."

# Start the application
echo "Starting the application..."
exec gunicorn --bind 0.0.0.0:4040 \
         --workers 3 \
         --threads 2 \
         --timeout 120 \
         --keep-alive 5 \
         --log-level info \
         --user www-data \
         "app:create_app()"

# #!/bin/sh

# # Wait for the database to be ready
# echo "Waiting for PostgreSQL..."
# while ! nc -z $DB_HOST 5432; do
#   sleep 1
# done
# echo "PostgreSQL started"

# # Wait an additional 5 seconds for the init script to complete
# sleep 5

# # Run migrations
# flask db upgrade

# # Start the application
# # gunicorn --bind 0.0.0.0:4040 "app:create_app()"
# gunicorn --bind 0.0.0.0:4040 \
#          --workers 3 \
#          --threads 2 \
#          --timeout 120 \
#          --keep-alive 5 \
#          --log-level info \
#          "app:create_app()"