from flask import Blueprint, jsonify, request, current_app
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from modules.library.models.requests import SignUpRequest, loginRequest, BookRequest
from modules.library.models.models import UserRoles
from modules.library.service import LibraryService
from functools import wraps


library_bp = Blueprint('library', __name__)

library_service = LibraryService()

# Set the expiration time for the token
expires = timedelta(minutes=15)

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

    login_request = loginRequest(**data)

    user = library_service.get_user_by_username(login_request.username)

    if not check_password_hash(user.password_hash, login_request.password):
        return jsonify({"error": "Invalid password"}), 400

    access_token = create_access_token(identity=user.id)

    return jsonify({"access_token": access_token}), 200

# Custom decorator for librarian access
def librarian_login_required(fn):
    @wraps(fn)
    @jwt_required()  # Require a valid JWT
    def decorator(*args, **kwargs):
        current_user_id = get_jwt_identity()  # Get user ID from the token
        current_user = library_service.get_user_by_id(current_user_id)

        if not current_user or current_user.role != UserRoles.LIBRARIAN.value:
            return jsonify({"error": "Access forbidden: Librarian role required"}), 403
        
        return fn(*args, **kwargs)
    return decorator

# Custom decorator for member access
def member_login_required(fn):
    @wraps(fn)
    @jwt_required()  # Require a valid JWT
    def decorator(*args, **kwargs):
        current_user_id = get_jwt_identity()  # Get user ID from the token
        current_user =  library_service.get_user_by_id(current_user_id)

        if not current_user or current_user.role != UserRoles.MEMBER.value:
            return jsonify({"error": "Access forbidden: Member role required"}), 403
        
        return fn(*args, **kwargs)
    return decorator

# Librarian routes

@library_bp.route('/books', methods=['GET'])
@jwt_required()
def get_books():
    books = library_service.get_books()
    return jsonify(books), 200

@library_bp.route('/add_book', methods=['POST'])
@librarian_login_required
def add_book():
    data = request.get_json()
    book_request = BookRequest(**data)

    # Add book to the database
    library_service.add_book(book_request)

    return jsonify({"message": "Book added successfully"}), 201