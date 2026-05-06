# Import SQLAlchemy for database ORM (Object Relational Mapping)
from flask_sqlalchemy import SQLAlchemy

# Import Migrate to handle database migrations (schema changes)
from flask_migrate import Migrate

# Import Bcrypt for password hashing (security for user passwords)
from flask_bcrypt import Bcrypt

# Import JWTManager for handling authentication tokens (login security)
from flask_jwt_extended import JWTManager


# Create database instance (used in models and queries)
db = SQLAlchemy()

# Create migration instance (tracks and applies database changes)
migrate = Migrate()

# Create bcrypt instance (used to hash and check passwords securely)
bcrypt = Bcrypt()

# Create JWT instance (used for token-based authentication)
jwt = JWTManager()