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

class JobsService:

    def get_job_post_data(self, job_id):
        job = Job.query.get(job_id)
        company = Company.query.get(job.company_id)
        
        if not job or not company:
            return None
        
        technologies = db.session.query(Technology.name).join(JobTechnology).filter(JobTechnology.job_id == job_id).all()
        tech_stack = [tech.name for tech in technologies]
        
        # Helper function to parse text to list
        def parse_text_to_list(text):
            if not text:
                return []
            try:
                return json.loads(text)
            except json.JSONDecodeError:
                return [item.strip() for item in text.split('\n') if item.strip()]

        return {
            'job_id': job.job_id,
            'title': job.title,
            'company': company.name,
            'company_id': company.company_id,
            'overview': job.overview,
            'responsibilities': parse_text_to_list(job.responsibilities),
            'requirements': parse_text_to_list(job.requirements),
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
    
    def filtered_search_jobs(self, filter_params, page, page_size):
        jobs_query = Job.query.join(Company)

        # Apply filters
        if filter_params['specialization']:
            jobs_query = jobs_query.filter(Job.specialization == filter_params['specialization'])
        if filter_params['experience_level']:
            jobs_query = jobs_query.filter(Job.experience_level == filter_params['experience_level'])
        if filter_params['min_experience_years']:
            jobs_query = jobs_query.filter(Job.min_experience_years >= int(filter_params['min_experience_years']))
        if filter_params['work_location']:
            jobs_query = jobs_query.filter(or_(Job.city.ilike(f"%{filter_params['work_location']}%"),
                                               Job.state.ilike(f"%{filter_params['work_location']}%"),
                                               Job.country.ilike(f"%{filter_params['work_location']}%")))
        if filter_params['industry']:
            jobs_query = jobs_query.filter(Job.industry == filter_params['industry'])
        if filter_params['salary_range']:
            jobs_query = jobs_query.filter(Job.salary_range == filter_params['salary_range'])
        if filter_params['city']:
            jobs_query = jobs_query.filter(Job.city.ilike(f"%{filter_params['city']}%"))
        if filter_params['tech_stack']:
            jobs_query = jobs_query.join(JobTechnology).join(Technology).filter(Technology.name.ilike(f"%{filter_params['tech_stack']}%"))

        total_jobs = jobs_query.count()
        jobs = jobs_query.order_by(Job.created_at.desc()).offset((page - 1) * page_size).limit(page_size).all()

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

        return results, total_jobs
    
    def instant_search_jobs(self, query, page, page_size):
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
                    'specialization': job.specialization,
                    'country': job.country,
                    'salary_range': job.salary_range,
                    'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
                    'experience_level': job.experience_level,
                    'min_experience_years': job.min_experience_years,
                    'tech_stack': tech_stack,
                    'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.company.logo_url)}",
                })

            return results, total_jobs
        else:
            return [], 0
        
    def get_home_page_jobs(self):
        specializations = ['Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity']
        
        all_jobs = {}
        for specialization in specializations:
            jobs = Job.query.join(Company).filter(Job.specialization == specialization).order_by(Job.created_at.desc()).limit(5).all()
            if jobs:
                jobs_list = []
                for job in jobs:
                    technologies = db.session.query(Technology.name).join(JobTechnology).filter(JobTechnology.job_id == job.job_id).all()
                    tech_stack = [tech.name for tech in technologies]

                    jobs_list.append({
                        'title': job.title,
                        'company': job.company.name,
                        'company_id': job.company_id,
                        'location': f"{job.city}, {job.state}",
                        'city': job.city,
                        'experience_level': job.experience_level,
                        'job_id': job.job_id,
                        'salary_range': job.salary_range,
                        'logo': f"{config.BASE_URL}/uploads/upload_company_logo/{os.path.basename(job.company.logo_url)}",
                        'specialization': job.specialization,
                        'min_experience_years': job.min_experience_years,
                        'created_at': get_relative_time(job.created_at.strftime('%Y-%m-%d')),
                        'tech_stack': tech_stack,
                        'jobpost_url': job.jobpost_url        
                    })
                
                all_jobs[specialization] = jobs_list
        
        return all_jobs
    
    def get_technologies(self):
        technologies = Technology.query.all()
        return [{"name": tech.name} for tech in technologies]

    # Apply to a particular job post
    def apply_to_job(self, userid, jobid):
        """
        Apply to a particular job post.
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
        """
        bookmark = Bookmark(userid=userid, jobid=jobid)
        db.session.add(bookmark)
        db.session.commit()

    def is_job_applied(self, user_id, job_id):
        application = Application.query.filter_by(userid=user_id, jobid=job_id).first()
        return application is not None

    def is_job_saved(self, user_id, job_id):
        bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
        return bookmark is not None

    def unsave_job(self, user_id, job_id):
        bookmark = Bookmark.query.filter_by(userid=user_id, jobid=job_id).first()
        if bookmark:
            db.session.delete(bookmark)
            db.session.commit()
        else:
            raise ValueError("Job was not saved")
        

    #--------------------------------------------------------------------------------
    
    # Retrieve a job post by its ID
    def get_job_by_id(self, job_id):
        """
        Retrieve a job post by its job_id
        :return: Return a Job object
        """
        return Job.query.get(job_id)
        
    def get_company_by_id(self, company_id):
        """
    Return a Company object by the company_id.
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