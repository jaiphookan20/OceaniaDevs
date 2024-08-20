from extensions import db
from models import Job, Recruiter, Company,Application, Bookmark
from flask import jsonify
from sqlalchemy import and_, func, or_ 

class JobsService:

    # Retrieve a job post by its ID
    def get_job_by_id(self, job_id):
        """
        Retrieve a job post by its ID using SQLAlchemy ORM.
        :param job_id: int - The ID of the job to fetch.
        :return: Job object or None if not found
        """
        return Job.query.get(job_id)
    
    # Return the list of all Recruiters
    def get_recruiters(self):
        """
        Return the list of all recruiters.
        :return: List of Recruiter objects
        """
        return Recruiter.query.with_entities(Recruiter.recruiter_id, Recruiter.first_name, Recruiter.last_name).all()

    # Return the list of all Companies
    def get_companies(self):
        """
        Return the list of all companies.
        :return: List of Company objects
        """
        return Company.query.with_entities(Company.company_id, Company.name).all()
    
    def get_company_by_id(self, company_id):
        """
        Return a Company object by the id.
        :return: Return a Company object
        """
        return Company.query.filter_by(company_id=company_id).first()
    
    def get_company_by_jobid(self, jobid):
        """
        Return a Company object by the jobid.
        :return: Return a Company object
        """
        job = Job.query.filter_by(job_id=jobid).first()
        return Company.query.filter_by(company_id=job.company_id).first()
    
    # Return the list of all available jobs along with job title, company name, job city, state, country
    # def get_available_jobs(self):
    #     """
    #     Return the list of all available jobs along with job_id, job title, company name, job city, state, and country.

    #     The structure of the job tuple is as follows:
    #     So, job[0] refers to the Job object instance, and job[0].job_id accesses the job_id attribute of that Job object instance.
    #     For example, if the job tuple looks like this:
    #     job = (
    #         <Job 5>,
    #         'Principal Frontend Software Engineer',
    #         'Atlassian',
    #         'Sydney',
    #         'NSW',
    #         'Australia'
    #     )
    #     Then, job[0] would be <Job 5>, which is the Job object instance with job_id 5. Therefore, job[0].job_id would give you the value 5.
    #     So, job[0].job_id represents the job_id of the specific Job object instance in that tuple, not the first job in the list.
    #     :return: List of tuples with job details
    #     """
    #     return Job.query.join(Company, Job.company_id == Company.company_id).add_columns(
    #         Job.job_id, Job.title, Company.name.label('company_name'), Job.city, Job.state, Job.country, Job.specialization, Job.experience_level, Job.tech_stack, Job.salary_range).all()
    
    def get_available_jobs(self):
            """
            Return the list of all available jobs along with job_id, job title, company name, job city, state, and country.

            The structure of the job tuple is as follows:
            So, job[0] refers to the Job object instance, and job[0].job_id accesses the job_id attribute of that Job object instance.
            For example, if the job tuple looks like this:
            job = (
                <Job 5>,
                'Principal Frontend Software Engineer',
                'Atlassian',
                'Sydney',
                'NSW',
                'Australia'
            )
            Then, job[0] would be <Job 5>, which is the Job object instance with job_id 5. Therefore, job[0].job_id would give you the value 5.
            So, job[0].job_id represents the job_id of the specific Job object instance in that tuple, not the first job in the list.
            :return: List of tuples with job details
            """
            return Job.query.join(Company, Job.company_id == Company.company_id).add_columns(
            Job.job_id, Job.title, Company.name.label('company_name'), Job.city, Job.state, Job.country, Job.specialization, Job.experience_level, Job.tech_stack, Job.salary_range).all()

    # Get Available Jobs (Pagination)
    def get_available_jobs_with_pagination(self, page, page_size):
        """
        Fetch available jobs with pagination.
        
        Args:
            page (int): The page number to fetch.
            page_size (int): The number of jobs per page.
        
        Returns:
            tuple: A tuple containing a list of jobs and the total job count.
        """
        try:
            print("Attempting to fetch jobs from database")
            offset = (page - 1) * page_size  # Calculate the offset for pagination
            
            # Join Job and Company tables to get job and company details
            jobs_query = db.session.query(Job, Company).join(Company, Job.company_id == Company.company_id)
            
            # Get the total number of jobs
            total_jobs = jobs_query.count()
            
            # Fetch jobs with pagination
            jobs = jobs_query.offset(offset).limit(page_size).all()
            
            return jobs, total_jobs
        except Exception as e:
            print(f"Error fetching jobs: {e}")
            return [], 0

    # Apply to a particular job post
    def apply_to_job(self, userid, jobid):
        """
        Apply to a particular job post.
        :param userid: int - ID of the user applying for the job.
        :param jobid: int - ID of the job to apply to.
        """
        try:
            application = Application(userid=userid, jobid=jobid)
            if application:
                application.status = "Applied";
                db.session.add(application)
                db.session.commit()
                return True
            return False
        except Exception as e:
            print(f"Error applying to job: {str(e)}")
            db.session.rollback()
            return False

    # Bookmark a particular job post
    def bookmark_job(self, userid, jobid):
        """
        Bookmark a particular job post.
        :param userid: int - ID of the user bookmarking the job.
        :param jobid: int - ID of the job to be bookmarked.
        """
        bookmark = Bookmark(userid=userid, jobid=jobid)
        db.session.add(bookmark)
        db.session.commit()

    # Filter jobs based on
    def filter_jobs(self, company_id=None, experience_level=None, industry=None, job_type=None, salary_range=None,
                work_location=None, min_experience_years=None, tech_stack=None, city=None, state=None,
                country=None, expiry_date=None, work_rights=None, specialization=None):
        """
        Filter jobs based on different criteria.
        """
        query = Job.query.join(Company, Job.company_id == Company.company_id).add_columns(
        Job.job_id, Job.title, Company.name.label('company_name'), Job.city, Job.state, Job.country,
        Job.work_location, Job.min_experience_years, Job.specialization, Job.experience_level
    )

        print("Inside filter_jobs service function")

        if company_id:
            query = query.filter(Job.company_id == company_id)
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        if industry:
            query = query.filter(Job.industry == industry)
        if job_type:
            query = query.filter(Job.job_type == job_type)
        if salary_range:
            query = query.filter(Job.salary_range == salary_range)
        if work_location:
            query = query.filter(Job.work_location == work_location)
        if min_experience_years is not None:
            query = query.filter(Job.min_experience_years >= min_experience_years)
        if tech_stack:
            query = query.filter(Job.tech_stack.contains(tech_stack))
        if city:
            query = query.filter(Job.city == city)
        if state:
            query = query.filter(Job.state == state)
        if country:
            query = query.filter(Job.country == country)
        if expiry_date:
            query = query.filter(Job.expiry_date == expiry_date)
        if work_rights:
            query = query.filter(Job.work_rights.contains(work_rights))
        if specialization:
            query = query.filter(Job.specialization == specialization)
        
        return query.all()
