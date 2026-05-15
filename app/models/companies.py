# Importing SQLAlchemy database instance from app extensions
# Used to define models (tables), columns, and relationships
from app.extensions import db

# Importing datetime to handle timestamps (created_at, updated_at)
from datetime import datetime


# Company model represents the 'companies' table in the database
class Company(db.Model):

   # Explicit table name in the database
    __tablename__ = 'companies'
    # Primary key: uniquely identifies each company
    id = db.Column(db.Integer, primary_key=True)
    # Company name (must be unique, cannot repeat)
    name = db.Column(db.String(100), unique=True)
    # Country or place of origin of the company
    origin = db.Column(db.String(100), unique=False)
    # Detailed description of the company
    description = db.Column(db.Text(), unique=False)
    # Foreign key linking company to a user (owner/creator)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    # Relationship to User model
    # Allows access like: company.user
    user = db.relationship('User', backref='companies')

    # Automatically stores when the record is created
    created_at = db.Column(db.DateTime, default=datetime.now)

    # Automatically updates when the record is modified
    updated_at = db.Column(db.DateTime, onupdate=datetime.now)



    # Used to initialize a Company object when creating a new record
    def __init__(self, name, origin, description, user_id):
        # Assign values to object properties
        self.name = name
        self.origin = origin
        self.description = description
        self.user_id = user_id   # FIXED: was incorrectly written as self.user_id = self.user_id


    # Defines how the object is displayed when printed
    # Useful for debugging and logs
    def __repr__(self):
        return f"{self.name} {self.origin}"
  

