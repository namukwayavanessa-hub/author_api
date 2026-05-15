# Import Blueprint for creating modular routes
from flask import Blueprint, jsonify

# Create an authentication blueprint (modular route group)
# All routes here will start with /api/auth
auth_bp = Blueprint("auth", __name__, url_prefix="/api/auth")


# Login route (POST method for sending login data)
@auth_bp.route("/login", methods=["POST"])
def login():
    # Placeholder response for login endpoint
    return jsonify({"message": "Login successful placeholder"}), 200