from app.extensions import db
from datetime import datetime

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(150), nullable=False)

    pages = db.Column(db.Integer, nullable=False)
    price_unit = db.Column(db.String(50), nullable=False, default='UGX')
    publication_date = db.Column(db.Date, nullable=False)

    isbn = db.Column(db.String(30), unique=True)
    genre = db.Column(db.String(255), nullable=False)
    image = db.Column(db.String(255))

    user_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    company_id = db.Column(db.Integer, db.ForeignKey('companies.id'))

    user = db.relationship('User', backref='books')
    company = db.relationship('Company', backref='books')

    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, onupdate=datetime.utcnow)

    def __init__(
        self,
        title,
        author_id,
        pages,
        publication_date,
        genre,
        user_id=None,
        company_id=None,
        price_unit='UGX',
        isbn=None,
        image=None
    ):
        self.title = title
        self.author_id = author_id
        self.pages = pages
        self.publication_date = publication_date
        self.genre = genre
        self.user_id = user_id
        self.company_id = company_id
        self.price_unit = price_unit
        self.isbn = isbn
        self.image = image

    def __repr__(self):
        return f"Book {self.title}"
    
    