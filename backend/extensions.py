from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_caching import Cache
from flask_mail import Mail

cache = Cache()
db = SQLAlchemy()
migrate = Migrate()
mail = Mail()  # Add this line
