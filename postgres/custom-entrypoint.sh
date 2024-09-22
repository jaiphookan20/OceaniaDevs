#!/bin/bash
set -e

# Start PostgreSQL in the background
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to become ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to become ready..."
  sleep 2
done

echo "PostgreSQL is ready, running post-init script..."

# Run the post-init script
/docker-entrypoint-initdb.d/post-init.sh

# Wait for the PostgreSQL process
wait $!