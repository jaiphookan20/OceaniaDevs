from extensions import bcrypt, db
from typing import Union
from sqlalchemy.dialects.postgresql import ENUM

class Seeker(db.Model):
    __tablename__ = 'seekers'

    uid = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(128))
    city = db.Column(db.String(255), nullable=False)
    state = db.Column(db.Enum('VIC', 'NSW', 'ACT', 'WA', 'QLD', 'NT', 'TAS', 'SA', name='state_enum'), nullable=False)
    country = db.Column(db.Enum('Australia', 'New Zealand', name='country_enum'), nullable=False)
    datetimestamp = db.Column(db.DateTime, default=db.func.current_timestamp())

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        result = bcrypt.check_password_hash(self.password_hash, password)
        print(f"Checking password: {password} against hash: {self.password_hash} - Result: {result}")
        return result
    
class Company(db.Model):
    __tablename__ = 'companies'
    company_id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    recruiters = db.relationship('Recruiter', backref='company', lazy=True)

class Recruiter(db.Model):
    __tablename__ = 'recruiters'
    recruiter_id = db.Column(db.Integer, primary_key=True)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), nullable=False)
    password = db.Column(db.String(255), nullable=False)
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    is_direct_recruiter = db.Column(db.Boolean)
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Job(db.Model):
    __tablename__ = 'jobs'
    job_id = db.Column(db.Integer, primary_key=True)
    recruiter_id = db.Column(db.Integer, db.ForeignKey('recruiters.recruiter_id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.company_id'))
    title = db.Column(db.String(255), nullable=False)
    description = db.Column(db.Text)
    specialization = db.Column(db.String(255))
    job_type = db.Column(ENUM('premium', 'normal', name='job_type'), default='normal')
    industry = db.Column(ENUM('Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare', 'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive', 'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism', 'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO', 'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics', name='industry_type'), nullable=False)
    salary_range = db.Column(ENUM('20000 - 40000', '40000 - 60000', '60000 - 80000', '80000 - 100000', '100000 - 120000', '120000 - 140000', '140000 - 160000', '160000 - 180000', '180000 - 200000', '200000 - 220000', '220000 - 240000', '240000 - 260000', '260000+', name='salary_range_type'))
    salary_type = db.Column(db.String(10))
    work_location = db.Column(db.String(20))
    min_experience_years = db.Column(db.Integer)
    experience_level = db.Column(db.String(50))
    tech_stack = db.Column(db.ARRAY(db.String))
    city = db.Column(db.String(255))
    state = db.Column(db.String(255))
    country = db.Column(db.String(255))
    expiry_date = db.Column(db.Date, server_default=db.text("CURRENT_DATE + INTERVAL '30 days'"))
    jobpost_url = db.Column(db.String(255))
    work_rights = db.Column(db.ARRAY(db.String))
    created_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())
    updated_at = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Application(db.Model):
    __tablename__ = 'applications'
    applicationid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())

class Bookmark(db.Model):
    __tablename__ = 'bookmarks'
    bookmarksid = db.Column(db.Integer, primary_key=True)
    userid = db.Column(db.Integer, db.ForeignKey('seekers.uid'))
    jobid = db.Column(db.Integer, db.ForeignKey('jobs.job_id'))
    datetimestamp = db.Column(db.DateTime, server_default=db.func.current_timestamp())


print("Models loaded")