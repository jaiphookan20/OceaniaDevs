from extensions import db
from models import Job, Recruiter, Company,Application, Bookmark

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

    
    # Return the list of all available jobs along with job title, company name, job city, state, country
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
            Job.job_id, Job.title, Company.name.label('company_name'), Job.city, Job.state, Job.country).all()
    
    # Apply to a particular job post
    def apply_to_job(self, userid, jobid):
        """
        Apply to a particular job post.
        :param userid: int - ID of the user applying for the job.
        :param jobid: int - ID of the job to apply to.
        """
        print("TYPE OF JOBID", type(jobid))
        application = Application(userid=userid, jobid=jobid)
        db.session.add(application)
        db.session.commit()

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
    def filter_jobs(self, company_id=None, experience_level=None, industry=None):
        """
        Filter jobs based on different criteria.
        """
        query = Job.query.join(Company, Job.company_id == Company.company_id).add_columns(
            Job.job_id, Job.title, Company.name.label('company_name'), Job.city, Job.state, Job.country)
        
        if company_id:
            query = query.filter(Job.company_id == company_id)
        if experience_level:
            query = query.filter(Job.experience_level == experience_level)
        if industry:
            query = query.filter(Job.industry == industry)

        return query.all()
    
    def populate_job_feed(self, uid, pagination_key, offset):
        # Implement the logic to populate the job feed based on user preferences
        pass