from modules.library.repository.models import User, Book, BorrowedBook, MemberHistory
from modules.library.models.requests import SignUpRequest, BookRequest
from app import db
from typing import List, Dict

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

    def get_user_by_id(self, user_id: str) -> User:
        return User.query.get(user_id)
    
    def add_book(self, book_request: BookRequest) -> None:
        new_book = Book(title=book_request.title, 
                        author=book_request.author, 
                        published_year=book_request.published_year)
        db.session.add(new_book)
        db.session.commit()

    def get_books(self) -> List[Dict]:
        books = Book.query.all()
        return [book.to_dict() for book in books]