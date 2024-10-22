**System Design:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/985ae735-6d10-43b6-be9a-8f4222482e2e)

**ERD Diagram:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/fa9d3504-6f96-4d30-967a-5f1d95cc06f9)

**Production Setup:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

**Development Setup:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```

**Staging Setup:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.staging.yml up --build

Job Board Application

This is a dockerized Job Board application with a React frontend, Flask backend, PostgreSQL database, and Redis for caching.
Prerequisites

Setup and Running the Application

**To stop the application:**
docker-compose down

**Build the application:**
docker compose build

**Run the application**
docker compose up

Contributing

Pull the latest changes from the main branch.
Create a new branch for your feature or bug fix.
Make your changes and test thoroughly.
Commit your changes and push to your branch.
Create a pull request for review.

Additional Notes

The first time you run the application, it may take a few moments to start as it needs to run database migrations.
Always pull the latest changes and run docker-compose up --build to ensure you have the most up-to-date version of the application.
If you make changes to requirements.txt, rebuild the backend container for the changes to take effect.
