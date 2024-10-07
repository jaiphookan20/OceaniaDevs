#!/bin/bash

set -x  # Enable debugging

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

echo "BACKUP_DIR: $BACKUP_DIR"
echo "DB_HOST: $DB_HOST"
echo "DB_USER: $DB_USER"
echo "DB_NAME: $DB_NAME"

if [ "$FLASK_ENV" = "staging" ]; then
    POSTGRES_DB="${POSTGRES_DB}_staging"
fi

mkdir -p "$BACKUP_DIR"

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

# Use the full path to pg_dump
PGPASSWORD=$DB_PASSWORD /usr/lib/postgresql/15/bin/pg_dump -h localhost -U $DB_USER -d $DB_NAME | gzip > "$BACKUP_DIR/pg_dump_$TIMESTAMP.sql.gz"

find "$BACKUP_DIR" -name "pg_dump_*.sql.gz" -type f -mtime +7 -delete