FROM ankane/pgvector:latest

# Create a custom initialization script
COPY ./init-pgvector.sql /docker-entrypoint-initdb.d/

# Set permissions for the init script
RUN chmod 0755 /docker-entrypoint-initdb.d/init-pgvector.sql