# Importing the database instance (SQLAlchemy) from app extensions
# This is used to define models, columns, and relationships
from app.extensions import db

# Importing datetime to handle timestamps (created_at, updated_at)
from datetime import datetime


# Book model represents the 'books' table in the database
class Book(db.Model):
    # Explicitly defining the table name in the database
    __tablename__ = 'books'



    # Primary key: uniquely identifies each book record
    id = db.Column(db.Integer, primary_key=True)

    # Book title (required field, max length 150 characters)
    title = db.Column(db.String(150), nullable=False)

    # Foreign key linking book to an author (authors.id)
    # This creates a relationship: one author can have many books
    # author_id = db.Column(db.Integer, db.ForeignKey('authors.id'), nullable=False)

    # Number of pages in the book
    pages = db.Column(db.Integer, nullable=False)

    # Currency unit for price (default is UGX)
    price_unit = db.Column(db.String(50), nullable=False, default='UGX')

    # Date when the book was published
    publication_date = db.Column(db.Date, nullable=False)

    # ISBN: unique identifier for books
    isbn = db.Column(db.String(30), unique=True)

    # Genre/category of the book (e.g. fiction, science, etc.)
    genre = db.Column(db.String(255), nullable=False)

    # Image path or URL for book cover
    image = db.Column(db.String(255))

    # Foreign key linking book to a user (who added/owns the book)
    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))

    # Foreign key linking book to a company (publisher/organization)
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))



    # Relationship to User model
    # Allows access like: book.user
    user = db.relationship('User', backref='books')

    # Relationship to Company model
    # Allows access like: book.company
    company = db.relationship('Company', backref='books')

    # Automatically stores when the record is created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # Automatically updates when the record is modified
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    # =========================
    # CONSTRUCTOR METHOD
    # =========================

    # Used to initialize a Book object when creating a new record
    def __init__(
        self,
        title,
        pages,
        publication_date,
        price,
        genre,
        description,
        user_id=None,
        company_id=None,
        price_unit='UGX',
        isbn=None,
        image=None
    ):
        # Assigning values to object properties
        self.title = title
        self.pages = pages
        self.publication_date = publication_date
        self.genre = genre
        # self.price =price
        self.user_id = user_id
        self.description =description
        self.company_id = company_id
        self.price_unit = price_unit
        self.isbn = isbn
        self.image = image


    # Defines how the object is displayed when printed
    # Useful for debugging and logging
    def __repr__(self):
        return f"Book {self.title}"
    
    