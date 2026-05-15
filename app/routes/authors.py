# Import Blueprint to organize routes into modular sections
# Import jsonify to return JSON responses from the API
from flask import Blueprint, jsonify

# Create Authors blueprint
# url_prefix ensures all routes start with /api/authors
authors_bp = Blueprint("authors", __name__, url_prefix="/api/authors")

# Test route to check if Authors API is working
# Endpoint: GET /api/authors/ping
@authors_bp.route("/ping")
def ping():

    # Returns a simple JSON response confirming the API is active
    return jsonify({"status": "ok", "message": "Authors API is running"}), 200

