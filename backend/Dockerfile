# Backend Dockerfile (backend/Dockerfile)
FROM python:3.9
WORKDIR /app
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt
COPY . .
EXPOSE 4040
CMD ["gunicorn", "--bind", "0.0.0.0:4040", "--config", "gunicorn_config.py", "app:create_app()"]