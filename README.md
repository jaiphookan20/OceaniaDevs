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
(venv) jai@192-168-1-100 aus-job-board % docker ps
CONTAINER ID   IMAGE                    COMMAND                  CREATED          STATUS          PORTS                    NAMES
864c1891a13c   aus-job-board-nginx      "/docker-entrypoint.…"   25 minutes ago   Up 25 minutes   0.0.0.0:80->80/tcp       aus-job-board-nginx-1
7bd9fd1cad1d   aus-job-board-frontend   "docker-entrypoint.s…"   25 minutes ago   Up 25 minutes   3000/tcp                 aus-job-board-frontend-1
685c43b4c24c   aus-job-board-backend    "./entrypoint.sh"        25 minutes ago   Up 25 minutes   0.0.0.0:4040->4040/tcp   aus-job-board-backend-1
f02da6704eec   aus-job-board-postgres   "docker-entrypoint.s…"   25 minutes ago   Up 25 minutes   0.0.0.0:5432->5432/tcp   aus-job-board-postgres-1
6f8cf5cb6fc1   redis:6                  "docker-entrypoint.s…"   25 minutes ago   Up 25 minutes   0.0.0.0:6379->6379/tcp   aus-job-board-redis-1

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
