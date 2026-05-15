from flask import Flask
from .config import Config
from app.extensions import db, migrate

# application factory function
def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)

    db.init_app(app)
    migrate.init_app(app, db)

    @app.route("/")
    def home():
        return {"message": "Authors API Project setup"}

    # Import models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book

    # Import blueprints
    from app.routes.authors import authors_bp
    from app.routes.books import books_bp

    # Register blueprints
    app.register_blueprint(authors_bp)
    app.register_blueprint(books_bp)

    return app