
# Product Overview:
![Screenshot 2024-07-03 at 10 39 56 PM](https://github.com/user-attachments/assets/bbb8bdf8-8de3-4066-81f7-336777789860)

## [Live URL](http://54.79.190.69/)

* OceaniaDevs is a new jobs platform focused entirely on the technology industry in Australia and dedicated to serving technology professionals. This job platform is meant to serve as a more precise and tailored alternative for frustrated job seekers in the technology industry with a far better discovery process than that provided by the dominant platforms.

## Technical Aspects:

Tools Used: Python, Flask, PostgreSQL, Javascript, Nginx, Redis, React, Github Actions, AWS

* Utilized **Python** and **Flask** with **Gunicorn** with the **Gevent** library for the backend
* Leveraged **PostgreSQL**’s Full-Text Search (FTS) capabilities and created indexes on key columns, resulting in a
∼80% improvement in search query execution times
* Configured **NGINX** as a reverse proxy, significantly boosting page load speeds
* Implemented **Redis** for session management and caching search queries, reducing average response times by 60%
* Utilized **Docker** for containerization, ensuring consistent development and deployment environments
* Built a **CI/CD** pipeline to automate the deployment of the dockerized application to **AWS** Lightsail using
**GitHub Actions**, streamlining updates and maintenance
* Developed a responsive frontend with **React** and **TailwindCSS**, ensuring a modern and user-friendly interface

# **System Design:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/985ae735-6d10-43b6-be9a-8f4222482e2e)

# **ERD Diagram:**
![image](https://github.com/jaiphookan20/OceaniaDevs/assets/52240311/fa9d3504-6f96-4d30-967a-5f1d95cc06f9)


## Notes:
* Borne out of my own frustrations with the job-search process here, I decided to build OceaniaDevs to scratch my own itch of using a more human-friendly jobs platform dedicated to tech professionals and their needs, with a richer, easier search process

* This has been a entirely solo effort from the start. Although at the very beginning, it was meant to be a group effort hence why 4 contributors are listed (with one commit each by them at the very start)

* Launched in a limited-beta release; the platform already has 25+ registered users and applications from candidates and growing each day. I am optimistic that this platform will grow to serve thousands more job seekers over the coming months once I release the application to the wider public in end-October.

* ### Upcoming Features:
* Candidate Database with rich, detailed profile of the technical skillset of each candidate
* Advanced Candidate Ranking & Recommender System for each job, for Recruiters by using the power of Vector Embeddings + Advanced ML & NLP techniques
* Automated Candidate Telephonic Qualification for Jobs through Outbound Sales AI Agent

# **Candidate Features:**

## **Home/Landing Page with Jobs displayed by Specialisation**
![Screenshot 2024-10-23 at 8 26 11 AM](https://github.com/user-attachments/assets/342264ff-2e8e-42a5-a007-3ba0da67e16f)

## **Job Search - Tailored Search & Filtering for Technology Roles:**
![Screenshot 2024-10-23 at 8 17 06 AM](https://github.com/user-attachments/assets/97d619a1-d45f-48f8-bdc1-c96f2207a456)

## **Search by Job Roles, Job Titles, and Companies Direct from the Search Bar:**
![Screenshot 2024-10-23 at 8 17 25 AM](https://github.com/user-attachments/assets/5f21bd51-f8fb-496e-87cf-4c4033282935)

## Advanced Job Filtering: Search by Specialisation, Flexibility, Location, Type, etc
![Screenshot 2024-10-23 at 8 19 34 AM](https://github.com/user-attachments/assets/a63beba0-922c-4b53-b3a7-45f2c26d4f2e)

## **Obtain the Tech Stack for Each Job Without Reading Through the Fine Print:**
![Screenshot 2024-10-23 at 8 20 44 AM](https://github.com/user-attachments/assets/4a7578d0-f5b2-48c0-a146-81156d6fe42e)

## **Filter Jobs on the Basis of Tech Stack:**
![Screenshot 2024-10-23 at 8 18 04 AM](https://github.com/user-attachments/assets/a7c56316-6ab0-494c-98a3-655d6e848625)

## Companies Search: 
![Screenshot 2024-10-23 at 8 24 05 AM](https://github.com/user-attachments/assets/241c3564-4ae5-4a56-8b4c-d64bb0b083c1)

## Company Page:
![Screenshot 2024-10-23 at 8 24 42 AM](https://github.com/user-attachments/assets/51fc30d6-e3fd-45a1-adae-e5d7fa9a89e9)

## **Human-Friendly Job Post Design & Features:** 

Top Half: 
![Screenshot 2024-10-23 at 12 02 53 PM](https://github.com/user-attachments/assets/796c76f7-f452-42a7-b6bb-6b3ddcca4b5d)

Middle: Requirements & Responsibilities 
![Screenshot 2024-10-23 at 12 03 01 PM](https://github.com/user-attachments/assets/9f6bc2a4-2098-4996-89a4-a9372c001df6)

Bottom: Tech Stack and Similar Jobs
![Screenshot 2024-10-23 at 12 03 21 PM](https://github.com/user-attachments/assets/00f5305c-3bac-45d8-b07f-cbe3afd4dcc4)

## **Saved Jobs: Bookmark & Save Jobs for Later:**
![Screenshot 2024-10-23 at 8 27 51 AM](https://github.com/user-attachments/assets/8b5c1fbd-795c-4ada-9410-0b881efb283f)

## **Applied Jobs: Apply to Jobs and Keep Track of Them:**
![Screenshot 2024-10-23 at 8 31 16 AM](https://github.com/user-attachments/assets/7c08f905-4058-40e1-b0f9-01a0c70a6af5)

## **Application Outcomes Tracker: Track & Update Application Outcomes in One Place**
![Screenshot 2024-10-23 at 8 33 10 AM](https://github.com/user-attachments/assets/cfdd5301-b602-459c-8a55-60aa5bd97ab3)

# **Recruiter Features**:

## Recruiter Dashboard:
![Screenshot 2024-10-23 at 8 39 43 AM](https://github.com/user-attachments/assets/7739dbee-21ae-4a6c-b47f-e5a111ec4446)

## Recruiter Dashboard: Keep Track of Active & Expired Jobs:
![Screenshot 2024-10-23 at 8 40 54 AM](https://github.com/user-attachments/assets/a195d7cd-2ab2-4792-b805-10184f2f2e1e)

## Recruiter Onboarding Step 1:
![Screenshot 2024-10-23 at 8 38 30 AM](https://github.com/user-attachments/assets/bfb875df-67ad-46cf-869f-302d92086a60)

## Recruiter Onboarding Step 2: Find Employer or Create New One
![Screenshot 2024-10-23 at 8 38 37 AM](https://github.com/user-attachments/assets/5179303d-68fc-4946-8601-19bbef59fc7b)

## Recruiter Onboarding: Register with Employer:
![Screenshot 2024-10-23 at 8 38 58 AM](https://github.com/user-attachments/assets/def89bf0-6b24-4ef4-b088-b33dbd6bf6ae)

## Recruiter Onboarding: Email Verification Step:
![Screenshot 2024-10-23 at 8 39 04 AM](https://github.com/user-attachments/assets/95252165-280e-4d49-ac7f-03716601fcfb)

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
```

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





