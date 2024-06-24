import random
from datetime import datetime, timedelta
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from models import Job, Company  # Import your SQLAlchemy models
from sqlalchemy.sql import func


# Set up the database engine and session
DATABASE_URL = "postgresql://jai:techboard@localhost/test_job_board"
engine = create_engine(DATABASE_URL)
Session = sessionmaker(bind=engine)
session = Session()

# List of sample companies
companies = [
    Company(name="Airwallex"),
    Company(name="OceaniaDevs"),
    Company(name="Xero"),
    Company(name="Canva"),
    Company(name="Atlassian"),
    Company(name="CultureAmp")
]

# List of valid industries
industries = [
    'Government', 'Banking & Financial Services', 'Fashion', 'Mining', 'Healthcare',
    'IT - Software Development', 'IT - Data Analytics', 'IT - Cybersecurity', 
    'IT - Cloud Computing', 'IT - Artificial Intelligence', 'Agriculture', 'Automotive',
    'Construction', 'Education', 'Energy & Utilities', 'Entertainment', 'Hospitality & Tourism',
    'Legal', 'Manufacturing', 'Marketing & Advertising', 'Media & Communications', 'Non-Profit & NGO',
    'Pharmaceuticals', 'Real Estate', 'Retail & Consumer Goods', 'Telecommunications', 'Transportation & Logistics'
]


# Add sample companies to the database
session.add_all(companies)
session.commit()

# List of sample job titles, locations, and tech stacks
job_titles = ["Software Engineer", "Backend Developer", "Frontend Developer", "DevOps Engineer", "Data Scientist"]
cities = ["Sydney", "Melbourne", "Brisbane", "Perth", "Adelaide"]
states = ["NSW", "VIC", "QLD", "WA", "SA"]
salary_ranges = [
    '20000 - 40000',
    '40000 - 60000',
    '60000 - 80000',
    '80000 - 100000',
    '100000 - 120000',
    '120000 - 140000',
    '140000 - 160000',
    '160000 - 180000',
    '180000 - 200000',
    '200000 - 220000',
    '220000 - 240000',
    '240000 - 260000',
    '260000+'
]

tech_stacks = [
  "aws", "docker", "gcp", "kubernetes", "angular", "terraform", "prometheus", "azure",
  "react", "nodejs", "python", "java", "csharp", "javascript", "typescript", "ruby",
  "go", "rust", "swift", "django", "flask", "rails", "spring", "dotnet", "mysql",
  "postgresql", "mongodb", "redis", "kafka", "git", "github", "gitlab", "jenkins",
  "travis", "vue", "redux", "webpack", "babel", "sass", "less", "jquery", "bootstrap",
  "tailwind", "materialui", "cplusplus", "php", "laravel", "symfony", "codeigniter",
  "ionic", "android", "firebase", "graphql", "apollostack", "elasticsearch", "nginx",
  "apache", "linux", "bash", "vim", "vscode", "intellij", "figma", "illustrator",
  "photoshop", "xd", "jira", "confluence", "slack", "trello"
]

company_id = [1, 2, 3, 4, 5, 6, 7, 8, 17];

# Function to generate a random job post
def generate_random_job():
    title = random.choice(job_titles)
    city = random.choice(cities)
    state = random.choice(states)
    company_id = random.choice([1, 2, 3, 4, 5, 6, 7, 8, 17])
    experience_level = random.choice(["Junior", "Mid", "Senior"])
    specialization = random.choice(["Backend", "Frontend", "DevOps", "FullStack"])
    salary_range = random.choice(salary_ranges)
    tech_stack = random.sample(tech_stacks, random.randint(1, 5))
    industry = random.choice(industries)
    created_at = datetime.utcnow() - timedelta(days=random.randint(1, 365))

    job = Job(
        title=title,
        company_id=company_id,
        city=city,
        state=state,
        experience_level=experience_level,
        specialization=specialization,
        salary_range=salary_range,
        tech_stack=tech_stack,
        industry=industry,
        created_at=created_at
    )

    # Generate the search vector based on the job title, specialization, city, company name, and tech stack
    search_text = ' '.join([title, specialization, city] + tech_stack)
    job.search_vector = func.to_tsvector('english', search_text)

    return job

# Generate and add a large number of job posts
for _ in range(1000):  # Adjust the number as needed
    job = generate_random_job()
    session.add(job)

# Commit the job posts to the database
session.commit()

print("Added a large number of job posts to the test database.")


