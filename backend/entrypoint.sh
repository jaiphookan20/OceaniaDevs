#!/bin/sh

echo "Printing all environment variables:"
env

echo "Specific checks for Auth0 variables:"
echo "AUTH0_DOMAIN: $AUTH0_DOMAIN"
echo "AUTH0_CLIENT_ID: $AUTH0_CLIENT_ID"
echo "AUTH0_CLIENT_SECRET is set: $(if [ -n "$AUTH0_CLIENT_SECRET" ]; then echo "Yes"; else echo "No"; fi)"
echo "APP_SECRET_KEY is set: $(if [ -n "$APP_SECRET_KEY" ]; then echo "Yes"; else echo "No"; fi)"

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
flask db init || echo "Flask DB already initialized"
flask db migrate -m "initial migration" || echo "Migration files already exist"
flask db upgrade

# Check if migrations were successful
if [ $? -ne 0 ]; then
    echo "Migration failed. Exiting..."
    exit 1
fi

echo "Migrations completed successfully."

# Start the application
echo "Starting the application..."
gunicorn --config gunicorn_config.py "app:create_app()"


# #!/bin/sh

# # Print environment variables for debugging
# echo "AUTH0_DOMAIN: $AUTH0_DOMAIN"
# echo "AUTH0_CLIENT_ID: $AUTH0_CLIENT_ID"
# echo "AUTH0_CLIENT_SECRET is set: $(if [ -n "$AUTH0_CLIENT_SECRET" ]; then echo "Yes"; else echo "No"; fi)"
# echo "APP_SECRET_KEY is set: $(if [ -n "$APP_SECRET_KEY" ]; then echo "Yes"; else echo "No"; fi)"

# # Wait for the database to be ready
# echo "Waiting for PostgreSQL..."
# while ! nc -z $DB_HOST 5432; do
#   sleep 1
# done
# echo "PostgreSQL started"

# # Wait an additional 10 seconds for the init script to complete
# sleep 10

# # # Ensure correct permissions for the app directory
# # chown -R www-data:www-data /app

# # # Run migrations without verbose output
# # echo "Running database migrations..."
# # su www-data -s /bin/sh -c "flask db upgrade"

# # # Check if migrations were successful
# # if [ $? -ne 0 ]; then
# #     echo "Migration failed. Exiting..."
# #     exit 1
# # fi

# # echo "Migrations completed successfully."
# flask db upgrade

# # Start the application
# echo "Starting the application..."

# # gunicorn --bind 0.0.0.0:4040 "app:create_app()"
# gunicorn --config gunicorn_config.py "app:create_app()"

# # exec gunicorn --bind 0.0.0.0:4040 \
# #          --workers 3 \
# #          --threads 2 \
# #          --timeout 120 \
# #          --keep-alive 5 \
# #          --log-level info \
# #          --user www-data \
# #          "app:create_app()"


# #!/bin/sh

# # Wait for the database to be ready
# # echo "Waiting for PostgreSQL..."
# # while ! nc -z $DB_HOST 5432; do
# #   sleep 1
# # done
# # echo "PostgreSQL started"

# # # Wait an additional 5 seconds for the init script to complete
# # sleep 5

# # # Run migrations
# # flask db upgrade

# # # Start the application
# # # gunicorn --bind 0.0.0.0:4040 "app:create_app()"
# # gunicorn --bind 0.0.0.0:4040 \
# #          --workers 3 \
# #          --threads 2 \
# #          --timeout 120 \
# #          --keep-alive 5 \
# #          --log-level info \
# #          "app:create_app()"