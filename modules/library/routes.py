from flask import Blueprint, jsonify, request, current_app, g
from werkzeug.security import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import datetime, timedelta
from modules.library.models.requests import SignUpRequest, loginRequest, BookRequest, UpdateMemberRequest
from modules.library.models.models import UserRoles
from modules.library.service import LibraryService
from functools import wraps
from config import Config


auth_bp = Blueprint('auth', __name__)
librarian_bp = Blueprint('librarian', __name__)
member_bp = Blueprint('member', __name__)

library_service = LibraryService()

# Set the expiration time for the token
expires = timedelta(minutes=int(Config.JWT_EXPIRATION_MINUTES))

@auth_bp.route('/signup', methods=['POST'])
def signup():
    data = request.get_json()
    user_request = SignUpRequest(**data)

    current_app.logger.info(f"Creating user: {user_request.password}") 

    if library_service.user_exists(user_request.username):
        return jsonify({"error": "Username already exists"}), 400

    library_service.create_user(user_request=user_request)

    return jsonify({"message": "User created successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.get_json()

    login_request = loginRequest(**data)

    user = library_service.get_user_by_username(login_request.username)

    if user.status == 'DELETED':
        return jsonify({"error": "User does not exist"}), 400

    if not check_password_hash(user.password_hash, login_request.password):
        return jsonify({"error": "Invalid password"}), 400

    access_token = create_access_token(identity=user.id, expires_delta=expires)

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
        g.user_id = current_user_id
        current_user =  library_service.get_user_by_id(current_user_id)

        if not current_user or current_user.role != UserRoles.MEMBER.value:
            return jsonify({"error": "Access forbidden: Member role required"}), 403
        
        return fn(*args, **kwargs)
    return decorator

# Librarian routes

@librarian_bp.route('/books', methods=['GET'])
@librarian_login_required
def get_books():
    books = library_service.get_books()
    return jsonify(books), 200

@librarian_bp.route('/add_book', methods=['POST'])
@librarian_login_required
def add_book():
    data = request.get_json()
    book_request = BookRequest(**data)

    # Add book to the database
    library_service.add_book(book_request)

    return jsonify({"message": "Book added successfully"}), 201

@librarian_bp.route('/delete_book', methods=['DELETE'])
@librarian_login_required
def delete_book():
    book_id = request.get_json().get('book_id')
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400
    library_service.delete_book(book_id)
    return jsonify({"message": "Book deleted successfully"}), 200

@librarian_bp.route('/update_book', methods=['PUT'])
@librarian_login_required
def update_book():
    data = request.get_json()
    book_id = data.get('book_id')
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400
    book_request = BookRequest(**data)
    library_service.update_book(book_id, book_request)
    return jsonify({"message": "Book updated successfully"}), 200

@librarian_bp.route('/add_member', methods=['POST'])
@librarian_login_required
def add_member():
    data = request.get_json()
    user_request = SignUpRequest(**data)

    if library_service.user_exists(user_request.username):
        return jsonify({"error": "Username already exists"}), 400

    user_request.role = UserRoles.MEMBER

    library_service.create_user(user_request=user_request)

    return jsonify({"message": "Member created successfully"}), 201

#Soft Delete
@librarian_bp.route('/delete_member', methods=['DELETE'])
@librarian_login_required
def delete_member():
    member_id = request.get_json().get('member_id')
    if not member_id:
        return jsonify({"error": "Member ID is required"}), 400
    library_service.delete_user(member_id)
    return jsonify({"message": "Member deleted successfully"}), 200

@librarian_bp.route('/update_member', methods=['PUT'])
@librarian_login_required
def update_member():
    data = request.get_json()
    member_id = data.get('member_id')
    if not member_id:
        return jsonify({"error": "Member ID is required"}), 400
    user_request = UpdateMemberRequest(**data)
    library_service.update_user(member_id, user_request)
    return jsonify({"message": "Member updated successfully"}), 200

@librarian_bp.route('/member_history', methods=['GET'])
@librarian_login_required
def member_history():
    member_id = request.args.get('member_id')
    if not member_id:
        return jsonify({"error": "Member ID is required"}), 400
    history = library_service.get_member_history(member_id)
    return jsonify(history), 200

@librarian_bp.route('/view_members', methods=['GET'])
@librarian_login_required
def view_members():
    members = library_service.get_members()
    return jsonify(members), 200

# Member routes

@member_bp.route('/available_books', methods=['GET'])
@member_login_required
def available_books():
    books = library_service.get_available_books()
    return jsonify(books), 200

@member_bp.route('/borrow_book', methods=['POST'])
@member_login_required
def borrow_book():
    data = request.get_json()
    user_id = g.user_id
    book_id = data.get('book_id')
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400
    library_service.borrow_book(book_id, user_id)
    return jsonify({"message": "Book borrowed successfully"}), 200

@member_bp.route('/return_book', methods=['POST'])
@member_login_required
def return_book():
    data = request.get_json()
    user_id = g.user_id
    book_id = data.get('book_id')
    if not book_id:
        return jsonify({"error": "Book ID is required"}), 400
    library_service.return_book(book_id, user_id)
    return jsonify({"message": "Book returned successfully"}), 200

@member_bp.route('/delete_account', methods=['DELETE'])
@member_login_required
def delete_account():
    user_id = g.user_id
    library_service.delete_user(user_id)
    # Logout the user
    return jsonify({"message": "Account deleted successfully"}), 200

@member_bp.route('/books_borrowed', methods=['get'])
@member_login_required
def books_borrowed():
    user_id = g.user_id
    history = library_service.get_borrowed_books(user_id)
    return jsonify(history), 200