#!/bin/bash
set -e

echo "Starting post-init.sh execution"

psql -v ON_ERROR_STOP=1 --username "$POSTGRES_USER" --dbname "$POSTGRES_DB" <<-EOSQL
    \echo 'Executing init-pgvector.sql'
    \i /docker-entrypoint-initdb.d/init-pgvector.sql

    \echo 'Verifying setup:'
    SELECT 'Function exists: ' || EXISTS(SELECT 1 FROM pg_proc WHERE proname = 'jobs_search_vector_update') AS function_exists;
    SELECT 'Trigger exists: ' || EXISTS(SELECT 1 FROM pg_trigger WHERE tgname = 'jobs_search_vector_update') AS trigger_exists;
    SELECT 'Column exists: ' || EXISTS(SELECT 1 FROM information_schema.columns WHERE table_name = 'jobs' AND column_name = 'search_vector') AS column_exists;
    SELECT 'Index exists: ' || EXISTS(SELECT 1 FROM pg_indexes WHERE indexname = 'jobs_search_vector_idx') AS index_exists;
    
    \echo 'Listing all indexes:'
    SELECT indexname, indexdef
    FROM pg_indexes
    WHERE tablename IN ('jobs', 'companies', 'technologies', 'job_technologies');
EOSQL

echo "Finished post-init.sh execution"