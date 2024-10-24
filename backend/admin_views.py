from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm
from flask_admin import BaseView, expose, AdminIndexView
from wtforms import PasswordField, StringField, SelectField
from wtforms.validators import DataRequired, ValidationError
from models import Seeker, Recruiter, Company, Job, Application, Bookmark, Technology, TechnologyAlias, JobTechnology
from flask import redirect, url_for, session
from sqlalchemy import func
from datetime import datetime, timedelta
from extensions import db
from flask import send_file
import csv
import io
from sqlalchemy.orm import joinedload
from flask import render_template
from flask import flash
from sqlalchemy.exc import IntegrityError

# Base class for secure views, ensuring only authorized users can access
class SecureModelView(ModelView):
    def is_accessible(self):
        if 'user' not in session:
            return False
        user = session['user']
        return user.get('type') == 'seeker' and user.get('userinfo', {}).get('email') == 'jaiphookan@gmail.com'

    def inaccessible_callback(self, name, **kwargs):
        return render_template('admin/unauthorized.html'), 403

# Secure index view for the admin panel
class SecureAdminIndexView(AdminIndexView):
    def is_accessible(self):
        if 'user' not in session:
            return False
        user = session['user']
        return user.get('type') == 'seeker' and user.get('userinfo', {}).get('email') == 'jaiphookan@gmail.com'

    def inaccessible_callback(self, name, **kwargs):
        return render_template('admin/unauthorized.html'), 403

    @expose('/')
    def index(self):
        if not self.is_accessible():
            return self.inaccessible_callback(name='index')
        # Your dashboard logic here
        return self.render('admin/index.html')

# Custom view for Seeker model
class SeekerView(SecureModelView):
    column_exclude_list = ['password_hash']  # Don't show password hash in list view
    form_excluded_columns = ['password_hash']  # Don't allow editing password hash
    column_searchable_list = ['email', 'first_name', 'last_name']  # Enable searching
    column_filters = ['state', 'country']  # Add filters

# Custom view for Recruiter model
class RecruiterView(SecureModelView):
    column_exclude_list = ['password']
    form_excluded_columns = ['password']
    column_searchable_list = ['email', 'first_name', 'last_name']
    column_filters = ['state', 'country', 'is_direct_recruiter']

# Custom view for Company model
class CompanyView(SecureModelView):
    column_searchable_list = ['name', 'website_url']
    column_filters = ['country', 'industry', 'state']

# Custom view for Job model
class JobView(SecureModelView):
    column_searchable_list = ['title', 'description']
    column_exclude_list = ['search_vector']
    column_filters = ['specialization', 'job_type', 'industry', 'experience_level', 'work_location']

class TechnologiesView(SecureModelView):
    column_list = ['id', 'name']
    form_columns = ['name']
    column_searchable_list = ['id', 'name']
    column_filters = ['id', 'name']

class TechnologyAliasView(SecureModelView):
    column_list = ['alias', 'technology.name']
    form_columns = ['alias', 'technology']
    column_labels = {'technology.name': 'Technology'}
    column_searchable_list = ['alias', 'technology.name']
    column_filters = ['technology.name']

class JobTechnologyView(SecureModelView):
    column_list = ['job.title', 'technology.name']
    form_columns = ['job', 'technology']
    column_labels = {'job.title': 'Job Title', 'technology.name': 'Technology'}
    column_searchable_list = ['job.title', 'technology.name']
    column_filters = ['job.title', 'technology.name']

    def on_model_change(self, form, model, is_created):
        # Check if the association already exists
        existing = JobTechnology.query.filter_by(job_id=model.job_id, technology_id=model.technology_id).first()
        if existing:
            raise ValidationError('This job-technology association already exists.')

    def create_model(self, form):
        try:
            model = self.model()
            form.populate_obj(model)
            self.session.add(model)
            self._on_model_change(form, model, True)
            self.session.commit()
        except ValidationError as ex:
            flash(str(ex), 'error')
            return False
        except IntegrityError:
            self.session.rollback()
            flash('This job-technology association already exists.', 'error')
            return False
        return model

    def update_model(self, form, model):
        try:
            form.populate_obj(model)
            self._on_model_change(form, model, False)
            self.session.commit()
        except ValidationError as ex:
            flash(str(ex), 'error')
            return False
        except IntegrityError:
            self.session.rollback()
            flash('This job-technology association already exists.', 'error')
            return False
        return True

# Custom view for Application model
class ApplicationView(SecureModelView):
    column_list = ['applicationid', 'seeker.email', 'job.title', 'job.company.name', 'datetimestamp', 'status']
    column_labels = {
        'applicationid': 'Application ID',
        'seeker.email': 'Seeker Email',
        'job.title': 'Job Title',
        'job.company.name': 'Company Name',
        'datetimestamp': 'Application Date',
        'status': 'Status'
    }
    column_searchable_list = ['seeker.email', 'job.title', 'job.company.name', 'status']
    column_filters = ['status', 'datetimestamp', 'job.title', 'job.company.name']
    column_sortable_list = ['applicationid', 'datetimestamp', 'status', ('seeker.first_name', 'seeker.first_name'), ('job.title', 'job.title'), ('job.company.name', 'job.company.name')]

    def get_query(self):
        return self.session.query(self.model).options(
            joinedload(Application.seeker),
            joinedload(Application.job).joinedload(Job.company)
        )

    def get_count_query(self):
        return self.session.query(func.count('*')).select_from(self.model)
    

# Dashboard view showing overview statistics
class DashboardView(BaseView):
    @expose('/')
    def index(self):
        today = datetime.now().date()
        week_ago = today - timedelta(days=7)
        month_ago = today - timedelta(days=30)

        def get_stats(start_date):
            return {
                'new_seekers': Seeker.query.filter(Seeker.datetimestamp >= start_date).count(),
                'new_recruiters': Recruiter.query.filter(Recruiter.created_at >= start_date).count(),
                'jobs_posted': Job.query.filter(Job.created_at >= start_date).count(),
                'jobs_saved': Bookmark.query.filter(Bookmark.datetimestamp >= start_date).count(),
                'jobs_applied': Application.query.filter(Application.datetimestamp >= start_date).count(),
            }

        daily_stats = get_stats(today)
        weekly_stats = get_stats(week_ago)
        monthly_stats = get_stats(month_ago)

        # Existing code for total counts and recent items
        total_jobs = Job.query.count()
        total_applications = Application.query.count()
        total_seekers = Seeker.query.count()
        total_recruiters = Recruiter.query.count()
        total_companies = Company.query.count()

        recent_jobs = Job.query.order_by(Job.created_at.desc()).limit(5).options(joinedload(Job.company)).all()
        recent_applications = Application.query.order_by(Application.datetimestamp.desc()).limit(5).options(
            joinedload(Application.seeker),
            joinedload(Application.job)
        ).all()

        top_companies = db.session.query(Company.name, func.count(Job.job_id).label('job_count')).\
            join(Job).group_by(Company.company_id).order_by(func.count(Job.job_id).desc()).limit(5).all()

        return self.render('admin/dashboard.html', 
                           total_jobs=total_jobs,
                           total_applications=total_applications,
                           total_seekers=total_seekers,
                           total_recruiters=total_recruiters,
                           total_companies=total_companies,
                           recent_jobs=recent_jobs,
                           recent_applications=recent_applications,
                           top_companies=top_companies,
                           daily_stats=daily_stats,
                           weekly_stats=weekly_stats,
                           monthly_stats=monthly_stats)

# Statistics view showing more detailed statistics
class StatisticsView(BaseView):
    @expose('/')
    def index(self):
        # Fetch various statistics
        total_seekers = Seeker.query.count()
        total_recruiters = Recruiter.query.count()
        total_jobs = Job.query.count()
        total_applications = Application.query.count()
        
        # Calculate recent activity (last 30 days)
        thirty_days_ago = datetime.now() - timedelta(days=30)
        recent_jobs = Job.query.filter(Job.created_at >= thirty_days_ago).count()
        recent_applications = Application.query.filter(Application.datetimestamp >= thirty_days_ago).count()
        
        # Get top companies by job postings
        top_companies = db.session.query(Company.name, func.count(Job.job_id).label('job_count')).\
            join(Job).group_by(Company.company_id).order_by(func.count(Job.job_id).desc()).limit(5).all()
        
        # Render statistics template with data
        return self.render('admin/statistics.html', 
                           total_seekers=total_seekers,
                           total_recruiters=total_recruiters,
                           total_jobs=total_jobs, 
                           total_applications=total_applications,
                           recent_jobs=recent_jobs,
                           recent_applications=recent_applications,
                           top_companies=top_companies)

# Report view for generating reports
class ReportView(BaseView):
    @expose('/')
    def index(self):
        # Render report page
        return self.render('admin/reports.html')

    @expose('/generate_job_report')
    def generate_job_report(self):
        # Fetch all jobs
        jobs = Job.query.all()
        
        # Create CSV file in memory
        output = io.StringIO()
        writer = csv.writer(output)
        
        # Write CSV header
        writer.writerow(['Job ID', 'Title', 'Company', 'Location', 'Created At'])
        # Write job data
        for job in jobs:
            writer.writerow([job.job_id, job.title, job.company.name, f"{job.city}, {job.state}", job.created_at])
        
        # Prepare file for download
        output.seek(0)
        return send_file(io.BytesIO(output.getvalue().encode('utf-8')),
                         mimetype='text/csv',
                         as_attachment=True,
                         attachment_filename='job_report.csv')


