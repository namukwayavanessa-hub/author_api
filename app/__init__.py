from flask import Flask
from config import Config
from app.extensions import db, migrate,jwt
from app.Controllers.auth.auth_controllers import auth
from app.Controllers.users.user_controllers import users
from app.Controllers.companies.company_controllers import companies
from app.Controllers.books.book_controllers import books

# application factory function
def create_app():
    #app instance
    app = Flask(__name__)
    app.config.from_object('config.Config')

    db.init_app(app)
    migrate.init_app(app, db)
    jwt.init_app(app)

    @app.route("/")
    def home():
        return {"message": "Authors API Project setup"}

    # Import models
    from app.models.users import User
    from app.models.companies import Company
    from app.models.books import Book

    # Import blueprints
    # from app.routes.authors import authors_bp
    # from app.routes.books import users_bp

    # Register blueprints
    app.register_blueprint(auth)
    app.register_blueprint(users)
    app.register_blueprint(companies)
    app.register_blueprint(books)


    return app