from extensions import db
from models import Job, Recruiter, Company,Application, Bookmark, Technology, JobTechnology
from flask import jsonify
from sqlalchemy import desc
from datetime import datetime, timedelta
import config
import os
from utils.time import get_relative_time
from sqlalchemy import or_, func
import json
from app import current_app

class JobsService:

    @staticmethod
    def _parse_text_to_list(text):
        """Parse text to list, handling JSON and plain text formats."""
        if not text:
            return []
        try:
            return json.loads(text)
        except json.JSONDecodeError:
            return [item.strip() for item in text.split('\n') if item.strip()]

    def get_job_post_data(self, job_id):
        """Retrieve detailed information for a specific job post."""
        try:
            job = Job.query.get(job_id)
            company = Company.query.get(job.company_id)
            
            if not job or not company:
                return None
            
            technologies = db.session.query(Technology.name).join(JobTechnology).filter(JobTechnology.job_id == job_id).all()
            tech_stack = [tech.name for tech in technologies]
            
            return {
                'job_id': job.job_id,
                'title': job.title,
                'company': company.name,
                'company_id': company.company_id,
                'overview': job.overview,
                'responsibilities': self._parse_text_to_list(job.responsibilities),
                'requirements': self._parse_text_to_list(job.requirements),
                'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(company.logo_url)}",
                'industry': job.industry,
                'salary_range': job.salary_range,
                'country': job.country,
                'specialization': job.specialization,
                'salary_type': job.salary_type,
                'work_location': job.work_location,
                'location': f"{job.city}, {job.state}",
                'min_experience_years': job.min_experience_years,
                'experience_level': job.experience_level,
                'city': job.city,
                'description': job.description,
                'company_description': company.description,
                'state': job.state,
                'work_rights': job.work_rights,
                'tech_stack': tech_stack,
                'daily_range': job.daily_range,
                'hourly_range': job.hourly_range,
                'contract_duration': job.contract_duration,
                'job_arrangement': job.job_arrangement,
                'jobpost_url': job.jobpost_url,
                'created_at': job.created_at,
            }
        except Exception as e:
            current_app.logger.error(f"Error in get_job_post_data: {str(e)}")
            raise
    
    def filtered_search_jobs(self, filter_params, page, page_size):
        """Search and filter jobs based on various criteria."""
        try:
            jobs_query = Job.query.join(Company)

            for key, value in filter_params.items():
                if value:
                    if key == 'work_location':
                        jobs_query = jobs_query.filter(or_(Job.city.ilike(f"%{value}%"),
                                                           Job.state.ilike(f"%{value}%"),
                                                           Job.country.ilike(f"%{value}%")))
                    elif key == 'tech_stack':
                        jobs_query = jobs_query.join(JobTechnology).join(Technology).filter(Technology.name.ilike(f"%{value}%"))
                    elif key == 'min_experience_years':
                        jobs_query = jobs_query.filter(Job.min_experience_years >= int(value))
                    else:
                        jobs_query = jobs_query.filter(getattr(Job, key) == value)

            total_jobs = jobs_query.count()
            jobs = jobs_query.order_by(Job.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

            return self._format_job_results(jobs), total_jobs
        except Exception as e:
            current_app.logger.error(f"Error in filtered_search_jobs: {str(e)}")
            raise
    
    def instant_search_jobs(self, query, page, page_size):
        """Perform an instant search on jobs based on a query string."""
        try:
            if query:
                search_terms = query.split()
                search_query = ' | '.join(search_terms)
                tsquery = func.to_tsquery('english', search_query)
                
                jobs_query = Job.query.join(Company).filter(
                    or_(
                        Job.search_vector.op('@@')(tsquery),
                        Company.name.ilike(f'%{query}%')
                    )
                ).order_by(func.ts_rank(Job.search_vector, tsquery).desc())

                total_jobs = jobs_query.count()
                jobs = jobs_query.offset((page - 1) * page_size).limit(page_size).all()

                return self._format_job_results(jobs), total_jobs
            else:
                return [], 0
        except Exception as e:
            current_app.logger.error(f"Error in instant_search_jobs: {str(e)}")
            raise
        
    def get_home_page_jobs(self):
        """Retrieve jobs for the home page, grouped by specialization."""
        try:
            specializations = ['Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity']
            
            all_jobs = {}
            for specialization in specializations:
                jobs = Job.query.join(Company).filter(Job.specialization == specialization).order_by(Job.created_at.desc()).limit(5).all()
                if jobs:
                    all_jobs[specialization] = self._format_job_results(jobs)
            
            return all_jobs
        except Exception as e:
            current_app.logger.error(f"Error in get_home_page_jobs: {str(e)}")
            raise

    def _format_job_results(self, jobs):
        """Format job results for API responses."""
        try:
            results = []
            for job in jobs:
                technologies = db.session.query(Technology.name).join(JobTechnology).filter(JobTechnology.job_id == job.job_id).all()
                tech_stack = [tech.name for tech in technologies]

                results.append({
                    'job_id': job.job_id,
                    'company_id': job.company_id,
                    'title': job.title,
                    'company': job.company.name,
                    'city': job.city,
                    'location': f"{job.city}, {job.state}",
                    'country': job.country,
                    'salary_range': job.salary_range,
                    'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
                    'experience_level': job.experience_level,
                    'specialization': job.specialization,
                    'min_experience_years': job.min_experience_years,
                    'tech_stack': tech_stack,
                    'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.company.logo_url)}",
                })
            return results
        except Exception as e:
            current_app.logger.error(f"Error in _format_job_results: {str(e)}")
            raise
    
    def get_technologies(self):
        """Retrieve a list of all available technologies."""
        try:
            technologies = Technology.query.all()
            return [{"name": tech.name} for tech in technologies]
        except Exception as e:
            current_app.logger.error(f"Error in get_technologies: {str(e)}")
            raise

    def apply_to_job(self, seeker_id, job_id):
        """Allow a seeker to apply for a job."""
        try:
            existing_application = Application.query.filter_by(userid=seeker_id, jobid=job_id).first()
            if existing_application:
                raise ValueError("You have already applied to this job")

            job = Job.query.get(job_id)
            if not job:
                raise ValueError("Job not found")
            
            new_application = Application(userid=seeker_id, jobid=job_id)
            db.session.add(new_application)
            db.session.commit()
        
        except Exception as e:
            current_app.logger.error(f"Error in apply_to_job: {str(e)}")
            db.session.rollback()
            raise

    def bookmark_job(self, seeker_id, job_id):
        """Allow a seeker to bookmark a job."""
        try:
            existing_bookmark = Bookmark.query.filter_by(userid=seeker_id, jobid=job_id).first()
            if existing_bookmark:
                raise ValueError("You have already bookmarked this job")

            job = Job.query.get(job_id)
            if not job:
                raise ValueError("Job not found")

            new_bookmark = Bookmark(userid=seeker_id, jobid=job_id)
            db.session.add(new_bookmark)
            db.session.commit()
        except Exception as e:
            current_app.logger.error(f"Error in bookmark_job: {str(e)}")
            db.session.rollback()
            raise

    def is_job_applied(self, user_id, job_id):
        """Check if a user has applied to a specific job."""
        try:
            application = Application.query.filter_by(userid=user_id, jobid=job_id).first()
            return application is not None
        except Exception as e:
            current_app.logger.error(f"Error in is_job_applied: {str(e)}")
            raise

    def is_job_saved(self, user_id, job_id):
        """Check if a user has bookmarked a specific job."""
        try:
            bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
            return bookmark is not None
        except Exception as e:
            current_app.logger.error(f"Error in is_job_saved: {str(e)}")
            raise

    def unsave_job(self, user_id, job_id):
        """Remove a job from a user's bookmarks."""
        try:
            bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
            if bookmark:
                db.session.delete(bookmark)
                db.session.commit()
            else:
                raise ValueError("Job was not saved")
        except Exception as e:
            current_app.logger.error(f"Error in unsave_job: {str(e)}")
            db.session.rollback()
            raise

    #--------------------------------------------------------------------------------
    
    # Retrieve a job post by its ID and return a Job object 
    def get_job_by_id(self, job_id):
        """
        Retrieve a job post by its job_id
        :return: Return a Job object
        """
        try:
            return Job.query.get(job_id)
        except Exception as e:
            current_app.logger.error(f"Error in get_job_by_id: {str(e)}")
            raise
    
    # Retrieve a Company object by the company_id
    def get_company_by_id(self, company_id):
        """
    Return a Company object by the company_id.
        :return: Return a Company object
        """
        try:
            return Company.query.filter_by(company_id=company_id).first()
        except Exception as e:
            current_app.logger.error(f"Error in get_company_by_id: {str(e)}")
            raise
    
    # Retrieve a Company object by the jobid
    def get_company_by_jobid(self, jobid):
        """
        Return a Company object by the jobid.
        :return: Return a Company object
        """
        try:
            job = Job.query.filter_by(job_id=jobid).first()
            return Company.query.filter_by(company_id=job.company_id).first()
        except Exception as e:
            current_app.logger.error(f"Error in get_company_by_jobid: {str(e)}")
            raise