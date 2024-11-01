from flask_admin.contrib.sqla import ModelView
from flask_admin.form import SecureForm, ImageUploadField
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
# from backend.scraper_manager import process_all_job_files
import logging
from werkzeug.utils import secure_filename
import os
from markupsafe import Markup
from wtforms.widgets import Select
from flask_admin.form.widgets import Select2Widget

from PIL import Image

logger = logging.getLogger(__name__)

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
    logger.info(f"Available image formats: {', '.join(Image.registered_extensions().keys())}")
    column_searchable_list = ['name', 'company_id']
    column_filters = ['country', 'industry', 'state', 'city', 'type', 'size']
    
    # Override the form fields to use SelectField
    form_overrides = {
        'country': SelectField,
        'industry': SelectField,
        'state': SelectField,
        'city': SelectField,
        'type': SelectField,
        'size': SelectField
    }

    # Configure the form arguments for each SelectField
    form_args = {
        'country': {
            'choices': [
                ('Australia', 'Australia'),
                ('New Zealand', 'New Zealand')
            ],
            'coerce': str
        },
        'industry': {
            'choices': [
                ('Government', 'Government'),
                ('Banking & Financial Services', 'Banking & Financial Services'),
                ('Fashion', 'Fashion'),
                ('Mining', 'Mining'),
                ('Healthcare', 'Healthcare'),
                ('IT - Software Development', 'IT - Software Development'),
                ('IT - Data Analytics', 'IT - Data Analytics'),
                ('IT - Cybersecurity', 'IT - Cybersecurity'),
                ('IT - Cloud Computing', 'IT - Cloud Computing'),
                ('IT - Artificial Intelligence', 'IT - Artificial Intelligence'),
                ('Agriculture', 'Agriculture'),
                ('Automotive', 'Automotive'),
                ('Construction', 'Construction'),
                ('Education', 'Education'),
                ('Energy & Utilities', 'Energy & Utilities'),
                ('Entertainment', 'Entertainment'),
                ('Hospitality & Tourism', 'Hospitality & Tourism'),
                ('Legal', 'Legal'),
                ('Manufacturing', 'Manufacturing'),
                ('Marketing & Advertising', 'Marketing & Advertising'),
                ('Media & Communications', 'Media & Communications'),
                ('Non-Profit & NGO', 'Non-Profit & NGO'),
                ('Pharmaceuticals', 'Pharmaceuticals'),
                ('Real Estate', 'Real Estate'),
                ('Retail & Consumer Goods', 'Retail & Consumer Goods'),
                ('Telecommunications', 'Telecommunications'),
                ('Transportation & Logistics', 'Transportation & Logistics')
            ],
            'coerce': str
        },
        'state': {
            'choices': [
                ('VIC', 'VIC'),
                ('NSW', 'NSW'),
                ('ACT', 'ACT'),
                ('WA', 'WA'),
                ('QLD', 'QLD'),
                ('NT', 'NT'),
                ('TAS', 'TAS'),
                ('SA', 'SA')
            ],
            'coerce': str
        },
        'city': {
            'choices': [
                ('Sydney', 'Sydney'),
                ('Melbourne', 'Melbourne'),
                ('Brisbane', 'Brisbane'),
                ('Perth', 'Perth'),
                ('Adelaide', 'Adelaide'),
                ('Gold Coast', 'Gold Coast'),
                ('Newcastle', 'Newcastle'),
                ('Canberra', 'Canberra'),
                ('Sunshine Coast', 'Sunshine Coast'),
                ('Wollongong', 'Wollongong'),
                ('Hobart', 'Hobart'),
                ('Geelong', 'Geelong'),
                ('Townsville', 'Townsville'),
                ('Cairns', 'Cairns'),
                ('Darwin', 'Darwin'),
                ('Launceston', 'Launceston'),
                ('Mackay', 'Mackay'),
                ('Rockhampton', 'Rockhampton'),
                ('Toowoomba', 'Toowoomba')
            ],
            'coerce': str
        },
        'type': {
            'choices': [
                ('Agency', 'Agency'),
                ('Company', 'Company')
            ],
            'coerce': str
        },
        'size': {
            'choices': [
                ('0-9', '0-9'),
                ('10-49', '10-49'),
                ('50-249', '50-249'),
                ('250-999', '250-999'),
                ('1000+', '1000+')
            ],
            'coerce': str
        }
    }

    # Logo handling configuration
    def _list_thumbnail_and_url(view, context, model, name):
        if not model.logo_url:
            return ''
        return Markup(f'<img src="{model.logo_url}" width="100"><br>{model.logo_url}')

    column_formatters = {
        'logo_url': _list_thumbnail_and_url
    }

    # Define the upload path as an absolute path
    upload_path = '/app/uploads/upload_company_logo'
    
    # Log the upload path
    logger.info(f"Upload path: {upload_path}")
    
    form_extra_fields = {
        'logo': ImageUploadField('Logo', 
                                base_path=upload_path,
                                url_relative_path='uploads/upload_company_logo/')
    }

    def on_model_change(self, form, model, is_created):
        logger.info(f"on_model_change called for company: {model.name}")
        if form.logo.data:
            logger.info(f"Logo data found: {form.logo.data}")
            # Get the uploaded file
            file_data = form.logo.data

            # Generate the new filename using lowercase company name
            new_filename = f"{model.name.lower().replace(' ', '_')}.webp"
            logger.info(f"New filename: {new_filename}")

            try:
                # Open the image using Pillow
                image = Image.open(file_data)
                logger.info(f"Image opened successfully. Format: {image.format}, Size: {image.size}, Mode: {image.mode}")

                # Convert to RGB if the image is in RGBA mode (for PNG files with transparency)
                if image.mode == 'RGBA':
                    logger.info("Converting RGBA image to RGB")
                    image = image.convert('RGB')

                # Save the file as WebP
                file_path = os.path.join(self.upload_path, new_filename)
                logger.info(f"Attempting to save file to: {file_path}")
                logger.info(f"Current working directory: {os.getcwd()}")
                logger.info(f"Upload path exists: {os.path.exists(self.upload_path)}")
                logger.info(f"Upload path is writable: {os.access(self.upload_path, os.W_OK)}")
                
                image.save(file_path, 'WEBP')
                logger.info(f"File saved successfully to {file_path}")

                # Verify the file was actually saved
                if os.path.exists(file_path):
                    logger.info(f"File exists at {file_path}")
                    logger.info(f"File size: {os.path.getsize(file_path)} bytes")
                else:
                    logger.warning(f"File does not exist at {file_path}")

                # Update the model's logo_url
                model.logo_url = f'/uploads/upload_company_logo/{new_filename}'
                logger.info(f"Updated logo_url: {model.logo_url}")
            except Exception as e:
                logger.error(f"Error processing logo: {str(e)}", exc_info=True)
                raise
        elif is_created:
            model.logo_url = None
            logger.info("No logo uploaded for new company")
        else:
            logger.info("No new logo uploaded for existing company")

    # Add this to ensure logo_url is displayed in the list view
    column_list = ['name', 'website_url', 'country', 'industry', 'logo_url']  # Add other fields as needed

    def process_logo(self, logo_file):
        image = Image.open(logo_file)
        
        if image.mode == 'RGBA':
            image = image.convert('RGB')
        
        image.thumbnail((400, 400))
        background = Image.new('RGB', (400, 400), (255, 255, 255))
        paste_position = ((400 - image.width) // 2, (400 - image.height) // 2)
        background.paste(image, paste_position)
        
        output = io.BytesIO()
        background.save(output, format='WEBP', quality=85)
        output.seek(0)
        return output

# Custom view for Job model
class JobView(SecureModelView):
    column_searchable_list = ['title', 'job_id', 'company.name']
    column_exclude_list = ['search_vector', 'description']
    column_filters = ['specialization', 'job_type', 'industry', 'experience_level', 'work_location']

    # Add company.name to be displayed in list view
    column_list = [
        'title', 
        'company.name',  # Display company name
        'city', 
        'state', 
        'specialization', 
        'job_type', 
        'industry', 
        'experience_level', 
        'work_location', 
        'min_experience_years', 
        'job_arrangement'
    ]
    
    # Add label for company.name column
    column_labels = {
        'company.name': 'Company'
    }

    # Override form fields to use SelectField
    form_overrides = {
        'specialization': SelectField,
        'job_type': SelectField,
        'industry': SelectField,
        'experience_level': SelectField,
        'work_location': SelectField,
        'job_arrangement': SelectField,
        'salary_type': SelectField,
        'contract_duration': SelectField,
        'daily_range': SelectField,
        'hourly_range': SelectField
    }

    # Add widget configuration
    form_widget_args = {
        'specialization': {
            'widget': Select2Widget()
        },
        'job_type': {
            'widget': Select2Widget()
        },
        'industry': {
            'widget': Select2Widget()
        },
        'experience_level': {
            'widget': Select2Widget()
        },
        'work_location': {
            'widget': Select2Widget()
        },
        'job_arrangement': {
            'widget': Select2Widget()
        },
        'salary_type': {
            'widget': Select2Widget()
        },
        'contract_duration': {
            'widget': Select2Widget()
        },
        'daily_range': {
            'widget': Select2Widget()
        },
        'hourly_range': {
            'widget': Select2Widget()
        }
    }

    # Configure form arguments for each SelectField
    form_args = {
        'specialization': {
            'choices': [
                ('Frontend', 'Frontend', {}),
                ('Backend', 'Backend', {}),
                ('Full-Stack', 'Full-Stack', {}),
                ('Mobile', 'Mobile', {}),
                ('Data & ML', 'Data & ML', {}),
                ('QA & Testing', 'QA & Testing', {}),
                ('Cloud & Infra', 'Cloud & Infra', {}),
                ('DevOps', 'DevOps', {}),
                ('Project Management', 'Project Management', {}),
                ('IT Consulting', 'IT Consulting', {}),
                ('Cybersecurity', 'Cybersecurity', {})
            ],
            'coerce': str
        },
        'job_type': {
            'choices': [
                ('normal', 'Normal', {}), 
                ('featured', 'Featured', {})
            ],
            'coerce': str
        },
        'industry': {
            'choices': [
                ('Government', 'Government', {}),
                ('Banking & Financial Services', 'Banking & Financial Services', {}),
                ('Fashion', 'Fashion', {}),
                ('Mining', 'Mining', {}),
                ('Healthcare', 'Healthcare', {}),
                ('IT - Software Development', 'IT - Software Development', {}),
                ('IT - Data Analytics', 'IT - Data Analytics', {}),
                ('IT - Cybersecurity', 'IT - Cybersecurity', {}),
                ('IT - Cloud Computing', 'IT - Cloud Computing', {}),
                ('IT - Artificial Intelligence', 'IT - Artificial Intelligence', {}),
                ('Agriculture', 'Agriculture', {}),
                ('Automotive', 'Automotive', {}),
                ('Construction', 'Construction', {}),
                ('Education', 'Education', {}),
                ('Energy & Utilities', 'Energy & Utilities', {}),
                ('Entertainment', 'Entertainment', {}),
                ('Hospitality & Tourism', 'Hospitality & Tourism', {}),
                ('Legal', 'Legal', {}),
                ('Manufacturing', 'Manufacturing', {}),
                ('Marketing & Advertising', 'Marketing & Advertising', {}),
                ('Media & Communications', 'Media & Communications', {}),
                ('Non-Profit & NGO', 'Non-Profit & NGO', {}),
                ('Pharmaceuticals', 'Pharmaceuticals', {}),
                ('Real Estate', 'Real Estate', {}),
                ('Retail & Consumer Goods', 'Retail & Consumer Goods', {}),
                ('Telecommunications', 'Telecommunications', {}),
                ('Transportation & Logistics', 'Transportation & Logistics', {})
            ],
            'coerce': str
        },
        'experience_level': {
            'choices': [
                ('Junior', 'Junior', {}),
                ('Mid-Level', 'Mid-Level', {}),
                ('Senior', 'Senior', {}),
                ('Executive', 'Executive', {})
            ],
            'coerce': str
        },
        'work_location': {
            'choices': [
                ('Remote', 'Remote', {}),
                ('Hybrid', 'Hybrid', {}),
                ('Office', 'Office', {})
            ],
            'coerce': str
        },
        'job_arrangement': {
            'choices': [
                ('Permanent', 'Permanent', {}),
                ('Contract/Temp', 'Contract/Temp', {}),
                ('Internship', 'Internship', {}),
                ('Part-Time', 'Part-Time', {})
            ],
            'coerce': str
        },
        'salary_type': {
            'choices': [
                ('annual', 'Annual', {}), 
                ('hourly', 'Hourly', {}), 
                ('daily', 'Daily', {})
            ],
            'coerce': str
        },
        'contract_duration': {
            'choices': [
                ('Not Listed', 'Not Listed', {}),
                ('0-3 months', '0-3 months', {}),
                ('4-6 months', '4-6 months', {}),
                ('7-9 months', '7-9 months', {}),
                ('10-12 months', '10-12 months', {}),
                ('12+ months', '12+ months', {})
            ],
            'coerce': str
        },
        'daily_range': {
            'choices': [
                ('Not Listed', 'Not Listed', {}),
                ('0-200', '0-200', {}),
                ('200-400', '200-400', {}),
                ('400-600', '400-600', {}),
                ('600-800', '600-800', {}),
                ('800-1000', '800-1000', {}),
                ('1000-1200', '1000-1200', {}),
                ('1200-1400', '1200-1400', {}),
                ('1400-1600', '1400-1600', {}),
                ('1600+', '1600+', {})
            ],
            'coerce': str
        },
        'hourly_range': {
            'choices': [
                ('Not Listed', 'Not Listed', {}),
                ('0-20', '0-20', {}),
                ('20-40', '20-40', {}),
                ('40-60', '40-60', {}),
                ('60-80', '60-80', {}),
                ('80-100', '80-100', {}),
                ('100-120', '100-120', {}),
                ('120-140', '120-140', {}),
                ('140-160', '140-160', {}),
                ('160+', '160+', {})
            ],
            'coerce': str
        }
    }

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


# class JobProcessingView(BaseView):
#     @expose('/')
#     def index(self):
#         return self.render('admin/job_processing.html')

#     @expose('/process', methods=['POST'])
#     def process_jobs(self):
#         try:
#             processed_jobs, errors = process_all_job_files()
#             if errors:
#                 error_message = "\n".join(errors)
#                 flash(f'Job processing completed with {len(errors)} errors. Processed {processed_jobs} jobs successfully. Errors: {error_message}', 'warning')
#                 logger.warning(f'Job processing completed with errors: {error_message}')
#             else:
#                 flash(f'Job processing completed successfully. Processed {processed_jobs} jobs.', 'success')
#                 logger.info(f'Job processing completed successfully. Processed {processed_jobs} jobs.')
#         except Exception as e:
#             flash(f'Error processing jobs: {str(e)}', 'error')
#             logger.error(f'Error in job processing: {str(e)}', exc_info=True)
#         return redirect(url_for('.index'))

















