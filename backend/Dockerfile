FROM python:3.9

# Install netcat
RUN apt-get update && apt-get install -y netcat-openbsd && rm -rf /var/lib/apt/lists/*
RUN apt-get update && apt-get install -y postgresql-client
RUN apt-get update && apt-get install -y curl

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

# Ensure the script is executable
RUN chmod +x entrypoint.sh

# Set the entrypoint
ENTRYPOINT ["/bin/sh", "entrypoint.sh"]