#!/bin/bash

set -e
set -o pipefail

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

export AWS_ACCESS_KEY_ID=$R2_ACCESS_KEY_ID
export AWS_SECRET_ACCESS_KEY=$R2_SECRET_ACCESS_KEY

echo "Syncing backups to R2..."
aws --endpoint-url $R2_ENDPOINT s3 sync $BACKUP_DIR s3://$R2_BUCKET/backups

echo "Cleaning up old local backups..."
find $BACKUP_DIR -type f -mtime +30 -delete

echo "Sync and cleanup completed successfully."