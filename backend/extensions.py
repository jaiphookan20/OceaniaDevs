from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_migrate import Migrate
from flask_caching import Cache

cache = Cache()

db = SQLAlchemy()
bcrypt = Bcrypt()
migrate = Migrate()
