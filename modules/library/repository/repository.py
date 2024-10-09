from modules.library.repository.models import User, Book, BorrowedBook, MemberHistory
from modules.library.models.requests import SignUpRequest
from app import db

class LibraryRepository:

    def get_user_by_username(self, username: str) -> User:
        return User.query.filter_by(username=username).first()
    
    def create_user(self, user_request: SignUpRequest) -> None:
        new_user = User(username=user_request.username, 
                        password_hash=user_request.password, 
                        role=user_request.role.value,
                        first_name=user_request.first_name, 
                        last_name=user_request.last_name)
        db.session.add(new_user)
        db.session.commit()