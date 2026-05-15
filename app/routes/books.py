# Import Blueprint to create a modular route group for books
from flask import Blueprint

# Create a Books blueprint
# This groups all book-related routes together.  All routes will start with /api/books
books_bp = Blueprint("books", __name__, url_prefix="/api/books")