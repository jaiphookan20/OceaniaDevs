# Backend Dockerfile (backend/Dockerfile)
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4040
CMD ["/bin/sh", "entrypoint.sh"]

# FROM python:3.9
# WORKDIR /app
# RUN apt-get update && apt-get install -y netcat-openbsd
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# COPY migrations /app/migrations
# COPY migrations/alembic.ini /app/alembic.ini
# RUN chmod +x entrypoint.sh
# EXPOSE 4040
# ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]

# FROM python:3.9
# WORKDIR /app
# RUN apt-get update && apt-get install -y netcat-openbsd
# COPY requirements.txt .
# RUN pip install --no-cache-dir -r requirements.txt
# COPY . .
# RUN chmod +x entrypoint.sh
# EXPOSE 4040
# ENTRYPOINT ["/bin/sh", "./entrypoint.sh"]