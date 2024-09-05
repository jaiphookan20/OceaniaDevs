from extensions import bcrypt, db
from sqlalchemy.dialects.postgresql import ENUM, TSVECTOR
from sqlalchemy import event, text
from sqlalchemy.schema import DDL
from pgvector.sqlalchemy import Vector

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

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password_hash, password)

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

class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.recruiter_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    # specialization = db.Column(db.String(255))
    specialization = db.Column(specialization_enum) #new
    job_type = db.Column(job_type_enum, default='normal')
    industry = db.Column(industry_enum, nullable=False)
    salary_range = db.Column(salary_range_enum)
    salary_type = db.Column(db.String(10))
    # work_location = db.Column(db.String(20))
    work_location = db.Column(work_location_enum) #new
    min_experience_years = db.Column(db.Integer)
    # experience_level = db.Column(db.String(50))
    experience_level = db.Column(experience_level_enum) #new
    tech_stack = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    expiry_date = db.Column(db.Date, server_default=db.text("CURRENT_DATE + INTERVAL '30 days'"))
    jobpost_url = db.Column(db.String(255))
    work_rights = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    search_vector = db.Column(TSVECTOR)
    embedding = db.Column(Vector(1536))
    overview = db.Column(db.Text)  # New field
    responsibilities = db.Column(db.Text)  # New field
    requirements = db.Column(db.Text)  # New field
    # job_arrangement = db.Column(db.String(255))  
    job_arrangement = db.Column(job_arrangement_enum) #new
    contract_duration =  db.Column(db.String(255))  # New field
    hourly_range=db.Column(db.String(255))  # New field
    daily_range=db.Column(db.String(255))  # New field

class Technology(db.Model):
    __tablename__ = 'technologies'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String, unique=True, nullable=False)

class TechnologyAlias(db.Model):
    __tablename__ = 'technology_aliases'
    alias = db.Column(db.String, primary_key=True)
    technology_id = db.Column(db.Integer, db.ForeignKey('technologies.id'), nullable=False)
    
    technology = db.relationship('Technology', backref=db.backref('aliases', lazy=True))

class JobTechnology(db.Model):
    __tablename__ = 'job_technologies'
    job_id = db.Column(db.Integer, db.ForeignKey('jobs.job_id'), primary_key=True)  # Updated foreign key reference
    technology_id = db.Column(db.Integer, db.ForeignKey('technologies.id'), primary_key=True)

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

class Application(db.Model):
    __tablename__ = 'applications'
    applicationid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    status = db.Column(db.String(50), default='Applied')  # New field

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    bookmarksid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())
