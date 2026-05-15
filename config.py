
#Import OS module to access environment variables
import os

# Import Path to handle file paths in a clean and safe way
from pathlib import Path

# Get the base directory of the project (root folder)
BASE_DIR = Path(__file__).resolve().parent


# Configuration class for the Flask application
class Config:

    # Secret key used for sessions, cookies, and security features
    # Uses environment variable if available, otherwise uses default value
    SECRET_KEY = os.environ.get("SECRET_KEY", "dev-secret")

    # Secret key used to sign JWT tokens for authentication
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY", "jwt-dev-secret")

    # 🗄 MySQL database connection
    # SQLAlchemy database connection string
    # Connects Flask app to MySQL database (authors_db)
    SQLALCHEMY_DATABASE_URI ="mysql+pymysql://root:@localhost/flask_authors_db"

    # Disables SQLAlchemy event tracking (improves performance)
    SQLALCHEMY_TRACK_MODIFICATIONS = False

