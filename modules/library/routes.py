from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime
from modules.library.models.requests import SignUpRequest
from modules.library.service import LibraryService


auth_bp = Blueprint('auth', __name__)
librarian_bp = Blueprint('librarian', __name__)
member_bp = Blueprint('member', __name__)

library_service = LibraryService()

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_request = SignUpRequest(**data)

    current_app.logger.info(f"Creating user: {user_request.password}") 

    if library_service.user_exists(user_request.username):
        return jsonify({"error": "Username already exists"}), 400

    library_service.create_user(user_request=user_request)

    return jsonify({"message": "User created successfully"}), 201

