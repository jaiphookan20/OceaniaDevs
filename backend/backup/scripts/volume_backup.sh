#!/bin/bash

set -e
set -o pipefail

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

if ! docker volume inspect $VOLUME_NAME > /dev/null 2>&1; then
    echo "Volume $VOLUME_NAME does not exist. Creating it..."
    docker volume create $VOLUME_NAME
else
    echo "Volume $VOLUME_NAME already exists."
fi

# Create some test data in the volume
docker run --rm -v $VOLUME_NAME:/data alpine sh -c "echo 'Test data' > /data/test.txt"

mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

echo "Creating volume backup..."
docker run --rm -v $VOLUME_NAME:/volume -v $BACKUP_DIR:/backup alpine tar -czf /backup/volume_backup_$TIMESTAMP.tar.gz -C /volume ./

echo "Cleaning up old volume backups..."
find $BACKUP_DIR -name "volume_backup_*.tar.gz" -type f -mtime +7 -delete

echo "Volume backup completed successfully."