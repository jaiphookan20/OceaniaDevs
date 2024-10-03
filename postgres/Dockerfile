FROM ankane/pgvector:latest

# Ensure the directory exists
RUN mkdir -p /docker-entrypoint-initdb.d

# Copy the initialization script
COPY ./init-pgvector.sql /docker-entrypoint-initdb.d/

# Copy the post-init script
COPY ./post-init.sh /docker-entrypoint-initdb.d/

# Copy the new entrypoint script
COPY ./custom-entrypoint.sh /usr/local/bin/

# Set permissions for the scripts
RUN chmod 0755 /docker-entrypoint-initdb.d/init-pgvector.sql
RUN chmod 0755 /docker-entrypoint-initdb.d/post-init.sh
RUN chmod 0755 /usr/local/bin/custom-entrypoint.sh

# Set the new entrypoint
ENTRYPOINT ["custom-entrypoint.sh"]
CMD ["postgres"]