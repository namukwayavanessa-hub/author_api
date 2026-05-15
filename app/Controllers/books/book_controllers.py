from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.extensions import db
from app.models.books import Book
from app.models.companies import Company
from app.models.users import User
from app.status_codes import (
    HTTP_200_OK, HTTP_201_CREATED, HTTP_400_BAD_REQUEST,
    HTTP_404_NOT_FOUND, HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR, HTTP_403_FORBIDDEN
)

books = Blueprint('books', __name__, url_prefix='/api/v1/books')


# =========================
# CREATE BOOK
# =========================
@books.route('/create', methods=['POST'])
@jwt_required()
def createBook():
    try:
        data = request.get_json() or {}

        title = data.get('title')
        pages = data.get('pages')
        publication_date = data.get('publication_date')
        price_unit = data.get('price_unit')
        genre = data.get('genre')
        isbn = data.get('isbn')
        company_id = data.get('company_id')
        image = data.get('image')

        user_id = int(get_jwt_identity())

        if not all([title, pages, publication_date, price_unit, genre, isbn, company_id]):
            return jsonify({"error": "All required fields are required"}), HTTP_400_BAD_REQUEST

        if Book.query.filter_by(title=title, user_id=user_id).first():
            return jsonify({"error": "Book already exists"}), HTTP_409_CONFLICT

        if Book.query.filter_by(isbn=isbn).first():
            return jsonify({"error": "ISBN already exists"}), HTTP_409_CONFLICT

        company = Company.query.get(company_id)
        if not company:
            return jsonify({"error": "Company not found"}), HTTP_404_NOT_FOUND

        new_book = Book(
            title=title,
            pages=pages,
            publication_date=publication_date,
            genre=genre,
            isbn=isbn,
            company_id=company_id,
            user_id=user_id,
            price_unit=price_unit,
            image=image
        )

        db.session.add(new_book)
        db.session.commit()

        return jsonify({
            "message": "Book created successfully",
            "book": {
                "id": new_book.id,
                "title": new_book.title,
                "isbn": new_book.isbn,
                "genre": new_book.genre,
                "price_unit": new_book.price_unit,
                "user_id": new_book.user_id,
                "company_id": new_book.company_id
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# GET ALL BOOKS
# =========================
@books.route('/', methods=['GET'])
@jwt_required()
def getAllBooks():
    try:
        all_books = Book.query.all()

        result = []
        for book in all_books:
            result.append({
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "genre": book.genre,
                "price_unit": book.price_unit,
                "user_id": book.user_id,
                "company_id": book.company_id
            })

        return jsonify({
            "message": "Books retrieved successfully",
            "total": len(result),
            "books": result
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# GET BOOK BY ID
# =========================
@books.route('/<int:book_id>', methods=['GET'])
@jwt_required()
def getBookById(book_id):
    try:
        book = Book.query.get(book_id)

        if not book:
            return jsonify({"message": "Book not found"}), HTTP_404_NOT_FOUND

        return jsonify({
            "message": "Book retrieved successfully",
            "book": {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "genre": book.genre,
                "price_unit": book.price_unit,
                "user_id": book.user_id,
                "company_id": book.company_id
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# UPDATE BOOK
# =========================
@books.route('/update/<int:book_id>', methods=['PUT', 'PATCH'])
@jwt_required()
def updateBookDetails(book_id):
    try:
        data = request.get_json() or {}

        book = Book.query.get(book_id)
        if not book:
            return jsonify({"message": "Book not found"}), HTTP_404_NOT_FOUND

        current_user = int(get_jwt_identity())
        logged_in_user = User.query.get(current_user)

        if not logged_in_user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        if logged_in_user.user_type != "admin" and book.user_id != current_user:
            return jsonify({"error": "Not authorized"}), HTTP_403_FORBIDDEN

        book.title = data.get("title", book.title)
        book.pages = data.get("pages", book.pages)
        book.price_unit = data.get("price_unit", book.price_unit)
        book.genre = data.get("genre", book.genre)
        book.isbn = data.get("isbn", book.isbn)
        book.image = data.get("image", book.image)
        book.publication_date = data.get("publication_date", book.publication_date)

        db.session.commit()

        return jsonify({
            "message": "Book updated successfully",
            "book": {
                "id": book.id,
                "title": book.title,
                "isbn": book.isbn,
                "genre": book.genre,
                "price_unit": book.price_unit,
                "user_id": book.user_id,
                "company_id": book.company_id
            }
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# DELETE BOOK
# =========================
@books.route('/delete/<int:book_id>', methods=['DELETE'])
@jwt_required()
def deleteBook(book_id):
    try:
        book = Book.query.get(book_id)

        if not book:
            return jsonify({"message": "Book not found"}), HTTP_404_NOT_FOUND

        current_user = int(get_jwt_identity())
        logged_in_user = User.query.get(current_user)

        if not logged_in_user:
            return jsonify({"error": "User not found"}), HTTP_404_NOT_FOUND

        if logged_in_user.user_type != "admin" and book.user_id != current_user:
            return jsonify({"error": "Not authorized"}), HTTP_403_FORBIDDEN

        db.session.delete(book)
        db.session.commit()

        return jsonify({
            "message": f"Book '{book.title}' deleted successfully"
        }), HTTP_200_OK

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR