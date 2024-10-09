from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from modules.library.models.requests import SignUpRequest
from modules.library.service import LibraryService


library_bp = Blueprint('library', __name__)

library_service = LibraryService()

@library_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_request = SignUpRequest(**data)

    current_app.logger.info(f"Creating user: {user_request.password}") 

    if library_service.user_exists(user_request.username):
        return jsonify({"error": "Username already exists"}), 400

    library_service.create_user(user_request=user_request)

    return jsonify({"message": "User created successfully"}), 201

@library_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    user = library_service.get_user_by_username(username)

    if not check_password_hash(user.password_hash, password):
        return jsonify({"error": "Invalid password"}), 400

    access_token = create_access_token(identity=username)

    return jsonify({"access_token": access_token}), 200