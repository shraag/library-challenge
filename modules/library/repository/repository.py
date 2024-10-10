from modules.library.repository.models import User, Book, MemberHistory
from modules.library.models.requests import SignUpRequest, BookRequest, UpdateMemberRequest
from modules.library.models.models import UserRoles, Action, BookStatus, UserStatus
from app import db
from typing import List, Dict
from datetime import datetime

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
    
    def delete_book(self, book_id: str) -> None:
        Book.query.filter_by(id=book_id).delete()
        db.session.commit()

    def update_book(self, book_id: str, book_request: BookRequest) -> None:
        Book.query.filter_by(id=book_id).update({
            'title': book_request.title,
            'author': book_request.author,
            'published_year': book_request.published_year,
            'updated_at': datetime.now()
        })
        db.session.commit()

    def delete_user(self, user_id: str) -> None:
        #soft delete
        User.query.filter_by(id=user_id).update({'status': UserStatus.DELETED.value})
        db.session.commit()

    def update_user(self, user_id: str, user_request: UpdateMemberRequest) -> None:
        if user_request.first_name:
            User.query.filter_by(id=user_id).update({'first_name': user_request.first_name})
        if user_request.last_name:
            User.query.filter_by(id=user_id).update({'last_name': user_request.last_name})
        if user_request.username:
            User.query.filter_by(id=user_id).update({'username': user_request.username})
        User.query.filter_by(id=user_id).update({'updated_at': datetime.now()})
        db.session.commit()

    def get_member_history(self, member_id: str) -> List[Dict]:
        member_history = MemberHistory.query.filter_by(member_id=member_id).all()
        return [history.to_dict() for history in member_history]
    
    def get_members(self) -> List[Dict]:
        members = User.query.filter_by(role=UserRoles.MEMBER.value).all()
        return [member.to_dict() for member in members]
    
    def get_available_books(self) -> List[Dict]:
        books = Book.query.filter_by(status=BookStatus.AVAILABLE.value).all()
        return [book.to_dict() for book in books]
    
    def borrow_book(self, book_id: str, member_id: str) -> None:
        member_history = MemberHistory(member_id=member_id, book_id=book_id, action=Action.BORROWED.value)
        db.session.add(member_history)
        db.session.commit()
        Book.query.filter_by(id=book_id).update({'status': BookStatus.BORROWED.value})
        db.session.commit()

    def return_book(self, book_id: str, member_id: str) -> None:
        member_history = MemberHistory(member_id=member_id, book_id=book_id, action=Action.RETURNED.value)
        db.session.add(member_history)
        db.session.commit()
        Book.query.filter_by(id=book_id).update({'status': BookStatus.AVAILABLE.value})
        db.session.commit()

    def get_borrowed_books(self, member_id: str) -> List[Dict]:
        borrowed_books = db.session.query(Book).join(MemberHistory, Book.id == MemberHistory.book_id) \
            .filter(MemberHistory.member_id == member_id, MemberHistory.action == Action.BORROWED.value).all()
        return [book.to_dict() for book in borrowed_books]