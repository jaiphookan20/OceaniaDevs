#!/bin/bash

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

if [ "$FLASK_ENV" = "staging" ]; then
    VOLUME_NAME="${VOLUME_NAME}_staging"
fi

mkdir -p $BACKUP_DIR

TIMESTAMP=$(date +"%Y%m%d_%H%M%S")

docker run --rm -v $VOLUME_NAME:/volume -v $BACKUP_DIR:/backup alpine tar -czf /backup/volume_backup_$TIMESTAMP.tar.gz -C /volume ./

find $BACKUP_DIR -name "volume_backup_*.tar.gz" -type f -mtime +7 -delete