from flask import Blueprint, request, jsonify
from app.status_codes import (
    HTTP_400_BAD_REQUEST,
    HTTP_409_CONFLICT,
    HTTP_500_INTERNAL_SERVER_ERROR,
    HTTP_201_CREATED,
    HTTP_401_UNAUTHORIZED,
    HTTP_200_OK
)

import validators
from app.models.users import User
from app.extensions import db, bcrypt
from flask_jwt_extended import create_access_token, create_refresh_token, jwt_required, get_jwt_identity

# auth blueprint
auth = Blueprint('auth', __name__, url_prefix='/api/v1/auth')


# =========================
# REGISTER USER
# =========================
@auth.route('/register', methods=['POST'])
def register_user():

    data = request.get_json()

    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact = data.get('contact')
    email = data.get('email')
    user_type = data.get('user_type', 'author')
    password = data.get('password')
    biography = data.get('biography', '') if user_type == "author" else ''

    # validations
    if not first_name or not last_name or not contact or not password or not email:
        return jsonify({"error": "All fields are required"}), HTTP_400_BAD_REQUEST

    if user_type == 'author' and not biography:
        return jsonify({"error": "Enter your author biography"}), HTTP_400_BAD_REQUEST

    if len(password) < 8:
        return jsonify({"error": "Password is too short"}), HTTP_400_BAD_REQUEST

    if not validators.email(email):
        return jsonify({"error": "Email is not valid"}), HTTP_400_BAD_REQUEST

    if User.query.filter_by(email=email).first():
        return jsonify({"error": "Email already in use"}), HTTP_409_CONFLICT

    if User.query.filter_by(contact=contact).first():
        return jsonify({"error": "Contact already in use"}), HTTP_409_CONFLICT

    try:
        # FIX: decode bcrypt hash
        hashed_password = bcrypt.generate_password_hash(password).decode('utf-8')

        new_user = User(
            first_name=first_name,
            last_name=last_name,
            password=hashed_password,
            email=email,
            contact=contact,
            biography=biography,
            user_type=user_type
        )

        db.session.add(new_user)
        db.session.commit()

        return jsonify({
            "message": f"{new_user.get_full_name()} has been created successfully",
            "user": {
                "id": new_user.id,
                "first_name": new_user.first_name,
                "last_name": new_user.last_name,
                "email": new_user.email,
                "contact": new_user.contact,
                "type": new_user.user_type,
                "biography": new_user.biography,
                "created_at": new_user.created_at
            }
        }), HTTP_201_CREATED

    except Exception as e:
        db.session.rollback()
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# LOGIN USER
# =========================
@auth.route('/login', methods=['POST'])
def login():

    data = request.get_json()

    email = data.get('email')
    password = data.get('password')

    try:

        if not email or not password:
            return jsonify({"message": "Email and password are required"}), HTTP_400_BAD_REQUEST

        user = User.query.filter_by(email=email).first()

        if not user:
            return jsonify({"message": "Invalid email address"}), HTTP_401_UNAUTHORIZED

        if not bcrypt.check_password_hash(user.password, password):
            return jsonify({"message": "Invalid password"}), HTTP_401_UNAUTHORIZED

        access_token = create_access_token(identity= str(user.id))
        refresh_token = create_refresh_token(identity=str(user.id))

        return jsonify({
            "message": "Login successful",
            "user": {
                "id": user.id,
                "username": user.get_full_name(),
                "email": user.email,
                "type": user.user_type,
                "access_token": access_token,
                "refresh_token": refresh_token
            }
        }), HTTP_200_OK

    except Exception as e:
        return jsonify({"error": str(e)}), HTTP_500_INTERNAL_SERVER_ERROR


# =========================
# REFRESH TOKEN
# =========================
@auth.route('/token/refresh', methods=['POST'])
@jwt_required(refresh=True)
def refresh():

    identity = get_jwt_identity()
    access_token = create_access_token(identity=identity)

    return jsonify({"access_token": access_token}), HTTP_200_OK