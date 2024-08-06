FROM ankane/pgvector:latest

# Ensure the directory exists
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy the initialization script
COPY ./init-pgvector.sql /docker-entrypoint-initdb.d/

# Set permissions for the init script
RUN chmod 0755 /docker-entrypoint-initdb.d/init-pgvector.sql

# Add a script to run after PostgreSQL starts
COPY ./post-init.sh /docker-entrypoint-initdb.d/
RUN chmod 0755 /docker-entrypoint-initdb.d/post-init.sh

# FROM ankane/pgvector:latest

# # Ensure the directory exists
# RUN mkdir -p /docker-entrypoint-initdb.d

# # Copy the initialization script
# COPY ./init-pgvector.sql /docker-entrypoint-initdb.d/

# # Set permissions for the init script
# RUN chmod 0755 /docker-entrypoint-initdb.d/init-pgvector.sql