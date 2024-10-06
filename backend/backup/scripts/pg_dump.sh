#!/bin/bash

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

if [ "$FLASK_ENV" = "staging" ]; then
    POSTGRES_DB="${POSTGRES_DB}_staging"
fi

mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

PGPASSWORD=$POSTGRES_PASSWORD pg_dump -h $DB_HOST -U $POSTGRES_USER -d $POSTGRES_DB | gzip > $BACKUP_DIR/pg_dump_$TIMESTAMP.sql.gz

find $BACKUP_DIR -name "pg_dump_*.sql.gz" -type f -mtime +7 -delete