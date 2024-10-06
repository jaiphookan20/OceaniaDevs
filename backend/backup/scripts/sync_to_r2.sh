#!/bin/bash

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

if [ "$FLASK_ENV" = "staging" ]; then
    POSTGRES_DB="${POSTGRES_DB}_staging"
fi

export AWS_ACCESS_KEY_ID=$R2_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$R2_SECRET_ACCESS_KEY

aws --endpoint-url $R2_ENDPOINT s3 sync $BACKUP_DIR s3://$R2_BUCKET/backups

find $BACKUP_DIR -type f -mtime +30 -delete