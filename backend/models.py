from extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import ENUM, TSVECTOR
from sqlalchemy import event, text
from sqlalchemy.schema import DDL
from pgvector.sqlalchemy import Vector
from sqlalchemy import UniqueConstraint

# Define all ENUM types
state_enum = ENUM('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum', create_type=False)
country_enum = ENUM('Australia', 'New Zealand', name='country_enum', create_type=False)
job_type_enum = ENUM('premium', 'normal', name='job_type', create_type=False)
industry_enum = ENUM('Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics', name='industry_type', create_type=False)
salary_range_enum = ENUM('Not Listed', '20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+', name='salary_range_type', create_type=False)
# type_enum=ENUM('Agency', 'Company', create_type=False);
# city_enum = ENUM('Sydney', 'Melbourne', 'Brisbane', 'Perth', 'Adelaide', 'Gold Coast', 'Newcastle', 'Canberra', 'Geelong', 'Hobart', 'Townsville', 'Cairns', 'Darwin', name='city_enum', create_type=False)
specialization_enum = ENUM('Frontend', 'Backend', 'Full-Stack', 'Mobile', 'Data & ML', 'QA & Testing', 'Cloud & Infra', 'DevOps', 'Project Management', 'IT Consulting', 'Cybersecurity', name='specialization_enum', create_type=False)
experience_level_enum = ENUM('Junior', 'Mid-Level', 'Senior', 'Executive', name='experience_level_enum', create_type=False)
work_location_enum = ENUM('Remote', 'Hybrid', 'Office', name='work_location_enum', create_type=False)
job_arrangement_enum = ENUM('Permanent', 'Contract/Temp', 'Internship', 'Part-Time', name='job_arrangement_enum', create_type=False)

salary_type_enum = ENUM('annual', 'hourly', 'daily', name='salary_type_enum', create_type=False)
contract_duration_enum = ENUM('Not Listed', '0-3 months', '4-6 months', '7-9 months', '10-12 months', '12+ months', name='contract_duration_enum', create_type=False)
daily_range_enum = ENUM('Not Listed', '0-200', '200-400', '400-600', '600-800', '800-1000', '1000-1200', '1200-1400', '1400-1600', '1600+', name='daily_range_enum', create_type=False)
hourly_range_enum = ENUM('Not Listed', '0-20', '20-40', '40-60', '60-80', '80-100', '100-120', '120-140', '140-160', '160+', name='hourly_range_enum', create_type=False)

# Define your models
class Seeker(db.Model):
    __tablename__ = 'seekers'

    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128)) # need to get rid of this
    city = db.Column(db.String(255))
    state = db.Column(state_enum)
    country = db.Column(country_enum)
    datetimestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    applications = db.relationship('Application', back_populates='seeker')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    recruiter_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    first_name = db.Column(db.String(255))
    last_name = db.Column(db.String(255))
    position = db.Column(db.String(255))
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255))
    city = db.Column(db.String(255))
    state = db.Column(state_enum)  # Changed to use ENUM
    country = db.Column(country_enum)  # Changed to use ENUM
    is_direct_recruiter = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __str__(self):
        return f"{self.first_name} {self.last_name}"

class Company(db.Model):
    __tablename__ = 'companies'
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    website_url = db.Column(db.String(255))
    country = db.Column(country_enum)  # Changed to use ENUM
    size = db.Column(db.String(100))
    address = db.Column(db.String(255))
    description = db.Column(db.Text)
    logo_url = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    recruiters = db.relationship('Recruiter', backref='company', lazy=True)
    # New fields:
    industry = db.Column(industry_enum);
    state = db.Column(state_enum);
    city = db.Column(db.String(255));
    type=db.Column(db.String(255));
    name_vector = db.Column(TSVECTOR)

    __table_args__ = (
        db.Index('companies_name_vector_idx', 'name_vector', postgresql_using='gin'),
    )

    def __str__(self):
        return self.name

class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.recruiter_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    company = db.relationship('Company', backref=db.backref('jobs', lazy='dynamic')) # Adding line to create the relationship
    title = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))

    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    expiry_date = db.Column(db.Date, server_default=db.text("CURRENT_DATE + INTERVAL '30 days'"))
    jobpost_url = db.Column(db.String(255))
    
    description = db.Column(db.Text)
    overview = db.Column(db.Text)  # New field
    responsibilities = db.Column(db.Text)  # New field
    requirements = db.Column(db.Text)  # New field

    work_location = db.Column(work_location_enum) #new
    work_rights = db.Column(db.ARRAY(db.String))
    job_arrangement = db.Column(job_arrangement_enum) #new

    specialization = db.Column(specialization_enum) #new
    job_type = db.Column(job_type_enum, default='normal')
    industry = db.Column(industry_enum, nullable=False)
    
    min_experience_years = db.Column(db.Integer)
    experience_level = db.Column(experience_level_enum) #new
    tech_stack = db.Column(db.ARRAY(db.String))
    
    salary_range = db.Column(salary_range_enum)
    salary_type = db.Column(salary_type_enum, default='annual')
    contract_duration = db.Column(contract_duration_enum, default='Not Listed')
    daily_range = db.Column(daily_range_enum, default='Not Listed')
    hourly_range = db.Column(hourly_range_enum, default='Not Listed')

    # Add these new fields
    citizens_or_pr_only = db.Column(db.Boolean, default=False)
    security_clearance_required = db.Column(db.Boolean, default=False)

    search_vector = db.Column(TSVECTOR)
    embedding = db.Column(Vector(1536))  

    job_technologies = db.relationship('JobTechnology', back_populates='job', lazy='joined')
    applications = db.relationship('Application', back_populates='job')

    __table_args__ = (
        db.Index('jobs_specialization_idx', 'specialization'),
        db.Index('jobs_experience_level_idx', 'experience_level'),
        db.Index('jobs_work_location_idx', 'work_location'),
        db.Index('jobs_city_idx', 'city'),
        db.Index('jobs_search_vector_idx', 'search_vector', postgresql_using='gin'),
    )

    def __str__(self):
        return f"{self.title} at {self.company.name}"
class Technology(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)
    name_vector = db.Column(TSVECTOR)

    # Add this line
    job_technologies = db.relationship('JobTechnology', back_populates='technology')

    __table_args__ = (
        db.Index('technologies_name_vector_idx', 'name_vector', postgresql_using='gin'),
    )

    def __str__(self):
        return self.name

class TechnologyAlias(db.Model):
    __tablename__ = 'technology_aliases'
    alias = db.Column(db.String, primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technologies.id'), nullable=False)
    
    technology = db.relationship('Technology', backref=db.backref('aliases', lazy=True))

    def __str__(self):
        return f"{self.alias} (alias for {self.technology.name})"

class JobTechnology(db.Model):
    __tablename__ = 'job_technologies'
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technologies.id'), primary_key=True)
    
    # Change these lines
    job = db.relationship('Job', back_populates='job_technologies')
    technology = db.relationship('Technology', back_populates='job_technologies')

    __table_args__ = (
        db.Index('job_technologies_job_id_idx', 'job_id'),
        db.Index('job_technologies_technology_id_idx', 'technology_id'),
        db.UniqueConstraint('job_id', 'technology_id', name='uq_job_technology'),
    )

    def __init__(self, job=None, technology=None):
        self.job = job
        self.technology = technology

    def __str__(self):
        return f"{self.job.title} - {self.technology.name}"

class Candidate(db.Model):
    __tablename__ = 'candidates'
    candidate_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255))
    years_experience = db.Column(db.Integer)
    position = db.Column(db.String(255))
    work_experience = db.Column(db.String(800))
    favorite_languages = db.Column(db.ARRAY(db.String))
    technologies = db.Column(db.ARRAY(db.String))
    embedding = db.Column(Vector(1536))

    def __str__(self):
        return self.name

class Application(db.Model):
    __tablename__ = 'applications'
    applicationid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Applied')

    seeker = db.relationship('Seeker', back_populates='applications')
    job = db.relationship('Job', back_populates='applications')

    def __str__(self):
        return f"Application {self.applicationid}: {self.status}"

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    bookmarksid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

    def __str__(self):
        return f"Bookmark {self.bookmarksid}"
