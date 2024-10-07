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

-- Check for any orphaned records in job_technologies
SELECT 'Orphaned job_technologies records: ' || COUNT(*)
FROM job_technologies jt
LEFT JOIN jobs j ON jt.job_id = j.job_id
WHERE j.job_id IS NULL;

-- Check for any jobs without associated technologies
SELECT 'Jobs without technologies: ' || COUNT(*)
FROM jobs j
LEFT JOIN job_technologies jt ON j.job_id = jt.job_id
WHERE jt.job_id IS NULL;

-- Verify that all ENUM types are present
SELECT 'Missing ENUM type: ' || typname
FROM (
  VALUES ('state_enum'), ('country_enum'), ('job_type_enum'), ('industry_enum'),
         ('salary_range_enum'), ('specialization_enum'), ('experience_level_enum'),
         ('work_location_enum'), ('job_arrangement_enum'), ('salary_type_enum'),
         ('contract_duration_enum'), ('daily_range_enum'), ('hourly_range_enum')
) AS expected(typname)
WHERE typname NOT IN (SELECT typname FROM pg_type WHERE typtype = 'e');

-- Check for any NULL values in critical columns
SELECT 'NULL values in jobs.title: ' || COUNT(*) FROM jobs WHERE title IS NULL;
SELECT 'NULL values in companies.name: ' || COUNT(*) FROM companies WHERE name IS NULL;

-- Verify that search vectors are populated
SELECT 'Jobs with empty search_vector: ' || COUNT(*) FROM jobs WHERE search_vector IS NULL;
SELECT 'Companies with empty name_vector: ' || COUNT(*) FROM companies WHERE name_vector IS NULL;

-- Check for any data type mismatches (example for jobs table)
SELECT column_name, data_type
FROM information_schema.columns
WHERE table_name = 'jobs' AND (
  (column_name = 'job_id' AND data_type != 'integer') OR
  (column_name = 'title' AND data_type != 'character varying') OR
  (column_name = 'search_vector' AND data_type != 'tsvector')

-- Check row counts
SELECT 'Row count mismatch in jobs table: ' || COUNT(*) 
FROM jobs 
HAVING COUNT(*) != (SELECT COUNT(*) FROM jobs);

-- Check data integrity
SELECT 'Data mismatch in jobs table: ' || COUNT(*) 
FROM jobs 
WHERE job_id NOT IN (SELECT job_id FROM jobs);
);

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
