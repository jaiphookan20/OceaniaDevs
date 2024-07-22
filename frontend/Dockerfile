# Build stage: First stage builds the React app
FROM node:14 as build
WORKDIR /app
COPY package*.json ./
RUN npm install
COPY . .
RUN npm run build

# Production stage: Second stage uses NGINX to serve the built files
FROM nginx:alpine

# Copy the built React app files from the 'build' stage to the NGINX HTML directory
COPY --from=build /app/build /usr/share/nginx/html 

# Expose port 80, which is the default HTTP port
EXPOSE 80

# Set the command to run when the container starts: This starts NGINX and keeps it running in the foreground
CMD ["nginx", "-g", "daemon off;"]
