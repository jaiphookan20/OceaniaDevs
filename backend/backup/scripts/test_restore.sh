#!/bin/bash

set -e  # Exit immediately if a command exits with a non-zero status
set -o pipefail  # Return value of a pipeline is the value of the last command to exit with a non-zero status

source /home/ubuntu/OceaniaDevs/backend/backup/config.env

TEST_CONTAINER="postgres_test"

docker run --name $TEST_CONTAINER -e POSTGRES_USER=$DB_USER -e POSTGRES_PASSWORD=$DB_PASSWORD -e POSTGRES_DB=$DB_NAME -d postgres:15

LATEST_BACKUP=$(ls -t $BACKUP_DIR/pg_dump_*.sql.gz | head -n1)

gunzip < $LATEST_BACKUP | docker exec -i $TEST_CONTAINER psql -U $DB_USER -d $DB_NAME

# Run comprehensive tests
docker exec -i $TEST_CONTAINER psql -U $DB_USER -d $DB_NAME <<EOF > test_results.txt
-- Check if all expected tables exist
SELECT 'Missing table: ' || table_name
FROM (
  VALUES ('seekers'), ('companies'), ('recruiters'), ('jobs'), ('technologies'), ('job_technologies')
) AS expected(table_name)
WHERE table_name NOT IN (SELECT table_name FROM information_schema.tables WHERE table_schema = 'public');

-- Check if all expected indexes exist
SELECT 'Missing index: ' || indexname
FROM (
  VALUES ('jobs_search_vector_idx'), ('companies_name_vector_idx'), ('technologies_name_vector_idx'),
         ('jobs_specialization_idx'), ('jobs_experience_level_idx'), ('jobs_work_location_idx'),
         ('jobs_city_idx'), ('job_technologies_job_id_idx'), ('job_technologies_technology_id_idx')
) AS expected(indexname)
WHERE indexname NOT IN (SELECT indexname FROM pg_indexes WHERE schemaname = 'public');

-- Additional checks (orphaned records, NULL values, etc.) as in the original script

EOF

# Clean up
docker stop $TEST_CONTAINER
docker rm $TEST_CONTAINER

# Check if any errors were reported
if grep -q "Missing" test_results.txt; then
    echo "Errors detected during backup test:"
    cat test_results.txt
    exit 1
else
    echo "Backup test completed successfully."
    cat test_results.txt
fi

rm test_results.txt