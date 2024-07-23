FROM nginx:alpine

# Create cache directory
RUN mkdir -p /var/cache/nginx

# Copy your custom Nginx configuration
COPY job-board.conf /etc/nginx/conf.d/default.conf

# Copy the built React app
COPY --from=aus-job-board-frontend:latest /usr/share/nginx/html /usr/share/nginx/html

EXPOSE 80 

CMD ["nginx", "-g", "daemon off;"]

# FROM nginx:alpine
# # Create cache directory
# RUN mkdir -p /var/cache/nginx
# COPY job-board.conf /etc/nginx/conf.d/default.conf
# RUN cat /etc/nginx/conf.d/default.conf