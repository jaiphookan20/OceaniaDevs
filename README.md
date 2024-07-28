**Production Setup:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.prod.yml up --build
```

**Development Setup:**

```bash
docker-compose -f docker-compose.yml -f docker-compose.dev.yml up --build
```


**ERD Diagram v1:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/fa9d3504-6f96-4d30-967a-5f1d95cc06f9)

**System Design v1:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/985ae735-6d10-43b6-be9a-8f4222482e2e)
**NOTE:** This is AI-generated as of right now (so I haven't looked in detail through the readme but added it for an initial guide)

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

**Accessing the application:**
Should be accessible by typing localhost on the browser

**Check the state of your containers:**
docker ps

Example:
![Screenshot 2024-07-08 at 4 56 26 AM](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/281039fa-d956-4bc2-96c4-19fa6c9c1590)

**Check out the tables of your DB**
docker exec -it aus-job-board-postgres-1 bash (REPLACE with name of image OR CONTAINER ID of your postgres container)

**Once you're inside the shell**:
psql -U jai -d job_board;
\dt; 

Development Workflow
Making Changes

**Frontend changes:**

Edit files in the frontend/ directory.
Changes will be reflected immediately due to volume mounting.


Backend changes:

Edit files in the backend/ directory.
Restart the backend container to apply changes:
Copydocker-compose restart backend



Database schema changes:

Make changes to your models in backend/models.py.
Generate a new migration:
Copydocker-compose exec backend flask db migrate -m "Description of changes"

Apply the migration:
Copydocker-compose exec backend flask db upgrade

Commit the new migration files to version control.



Useful Docker Commands

View logs of a specific service:
Copydocker-compose logs -f <service-name>
Replace <service-name> with frontend, backend, postgres, or redis.
Access the PostgreSQL database:
Copydocker-compose exec postgres psql -U jai -d job_board

Run a Flask shell:
Copydocker-compose exec backend flask shell


Troubleshooting

If you encounter database connection issues, ensure that the DB_HOST, DB_NAME, DB_USER, and DB_PASSWORD in your .env file match the values in docker-compose.yml for the postgres service.
If changes to the backend are not reflecting, try rebuilding the backend container:
Copydocker-compose up -d --build backend

If you need to reset the database, you can remove the volume and recreate it:
Copydocker-compose down -v
docker-compose up --build
Note: This will delete all data in the database.

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
