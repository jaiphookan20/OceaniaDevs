from database import PostgresDB
from extensions import db, bcrypt
from models import Job, Recruiter, Company

class RecruiterService:

    # Add a Job Post to the Jobs table
    def add_job(self, recruiter_id, company_id, title, description, specialization, job_type, industry, salary_range, salary_type, work_location, min_experience_years, experience_level, tech_stack, city, state, country, jobpost_url, work_rights):
        """
        Add a Job Post to the Jobs table.
        """
        new_job = Job(
            recruiter_id=recruiter_id,
            company_id=company_id,
            title=title,
            description=description,
            specialization=specialization,
            job_type=job_type,
            industry=industry,
            salary_range=salary_range,
            salary_type=salary_type,
            work_location=work_location,
            min_experience_years=min_experience_years,
            experience_level=experience_level,
            tech_stack=tech_stack,
            city=city,
            state=state,
            country=country,
            jobpost_url=jobpost_url,
            work_rights=work_rights
        )
        db.session.add(new_job)
        db.session.commit()

    # Add a new Recruiter to the Recruiters table
    def add_recruiter(self, company_id, first_name, last_name, email, password, city, state, country, is_direct_recruiter):
        """
        Add a new Recruiter to the Recruiters table.
        :param company_id: int - Company ID the recruiter belongs to.
        :param is_direct_recruiter: bool - Indicates if the recruiter is a direct recruiter.
        """
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')
        new_recruiter = Recruiter(
            company_id=company_id,
            first_name=first_name,
            last_name=last_name,
            email=email,
            password=hashed_password,
            city=city,
            state=state,
            country=country,
            is_direct_recruiter=is_direct_recruiter
        )
        db.session.add(new_recruiter)
        db.session.commit()


    # Add a new Company to the Companies table
    def add_company(self, name, city, state, country):
        """
        Add a new Company to the Companies table.
        :param name: str - Name of the company.
        :param city: str - City where the company is located.
        :param state: str - State where the company is located.
        :param country: str - Country where the company is located.
        """
        new_company = Company(
            name=name,
            city=city,
            state=state,
            country=country
        )
        db.session.add(new_company)
        db.session.commit()

    # Retrieve all job posts by a Recruiter
    def get_all_jobs_by_recruiter(self, recruiter_id):
        """
        Retrieve all job posts posted by a recruiter.
        :param recruiter_id: int - The ID of the recruiter to fetch.
        """
        return Job.query.filter_by(recruiter_id=recruiter_id).all()

    # Update a job post with given updates
    def update_job(self, job_id, data):
        """
        Update a job post with given updates.
        :param job_id: int - The ID of the job to be updated.
        :param data: dict - A dictionary containing the fields to update with their new values.
        """
        job = Job.query.get(job_id)
        if not job:
            return None
        
        for key, value in data.items():
            setattr(job, key, value)
        
        db.session.commit()
        return job


