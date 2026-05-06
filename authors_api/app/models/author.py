from app.extensions import db
from datetime import datetime

# Define the Author model (represents the 'authors' table in the database)
class Author(db.Model):
    __tablename__ = 'authors'
    __tablename__ = 'authors'  # Explicit table name in the database

    # Primary key: uniquely identifies each author
    id = db.Column(db.Integer, primary_key=True)

    # Author's first name (required field)
    first_name = db.Column(db.String(50), nullable=False)

    # Author's last name (required field)
    last_name = db.Column(db.String(50), nullable=False)

    # Contact information (optional field)
    contact = db.Column(db.String(50))

    # Timestamp for when the record was created
    created_at = db.Column(db.DateTime, default=datetime.utcnow)

    # One-to-many relationship:
    # One author can have many books 
books = db.relationship(
        'Book',
        backref='author',
        lazy=True,
        cascade='all, delete-orphan'
    )

@property
def as_json(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "contact": self.contact,
            "books": [
                {
                    "id": book.id,
                    "title": book.title,
                    "isbn": book.isbn
                } for book in self.books
            ]
        }    