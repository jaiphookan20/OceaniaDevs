#!/bin/bash
set -e

# Start PostgreSQL
docker-entrypoint.sh postgres &

# Wait for PostgreSQL to become ready
until pg_isready -U "$POSTGRES_USER" -d "$POSTGRES_DB"; do
  echo "Waiting for PostgreSQL to become ready..."
  sleep 2
done

echo "PostgreSQL is ready, running initialization scripts..."

# Run the initialization scripts
for f in /docker-entrypoint-initdb.d/*; do
  case "$f" in
    *.sql)    echo "$0: running $f"; psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" -f "$f" ;;
    *.sh)     echo "$0: running $f"; . "$f" ;;
    *)        echo "$0: ignoring $f" ;;
  esac
done

# Wait for the PostgreSQL process
wait $!