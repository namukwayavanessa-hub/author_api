from flask import Blueprint, jsonify
authors_bp = Blueprint("authors", __name__, url_prefix="/api/authors")
@authors_bp.route("/ping")
def ping():
 return jsonify({"status": "ok", "message": "Authors API is running"}),
200

