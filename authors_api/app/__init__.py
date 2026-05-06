from flask import Flask
from .config import Config
from app.extensions import db, migrate, bcrypt

def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)
    bcrypt.init_app(app)  

    @app.route("/")
    def home():
        return {"message": "Authors API Project setup"}  

    # Import ALL models
    from app.models.author import Author
    from app.models.books import Book
    from app.models.companies import Company
    from app.models.users import User

    # Import blueprints
    from app.routes.auth import auth_bp
    from app.routes.authors import authors_bp
    from app.routes.books import books_bp

    # Register blueprints
    app.register_blueprint(auth_bp)
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)

    return app