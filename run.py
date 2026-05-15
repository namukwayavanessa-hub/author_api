# Import application factory (creates Flask app) and database instance
from app import create_app, db

# Create the Flask application instance
app = create_app()

# Create application context (required to access database outside request)
with app.app_context():
    # Automatically creates alltables defined in models
      db.create_all()

# Starts the Flask development server
# debug=True enables auto-reload and detailed error messages
if __name__ == "__main__":
    app.run(debug=True)