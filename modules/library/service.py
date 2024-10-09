from modules.library.repository.repository import LibraryRepository
from modules.library.models.requests import SignUpRequest, BookRequest, UpdateMemberRequest
from modules.library.repository.models import User, Book, BorrowedBook, MemberHistory
from typing import List, Dict

library_repository = LibraryRepository()
class LibraryService:

    def user_exists(self, username: str) -> bool:
        if library_repository.get_user_by_username(username) is not None:
            return True
        return False
    
    def create_user(self, user_request: SignUpRequest) -> None:
        library_repository.create_user(user_request)

    def get_user_by_username(self, username: str) -> User:
        return library_repository.get_user_by_username(username)
    
    def get_user_by_id(self, user_id: str) -> User:
        return library_repository.get_user_by_id(user_id)
    
    def add_book(self, book_request: BookRequest) -> None:
        library_repository.add_book(book_request)

    def get_books(self) -> List[Dict]:
        return library_repository.get_books()
    
    def delete_book(self, book_id: str) -> None:
        library_repository.delete_book(book_id)

    def update_book(self, book_id: str, book_request: BookRequest) -> None:
        library_repository.update_book(book_id, book_request)
    
    def delete_user(self, user_id: str) -> None:
        library_repository.delete_user(user_id)

    def update_user(self, member_id: str, user_request: UpdateMemberRequest) -> None:
        return library_repository.update_user(member_id, user_request)
    
    def get_member_history(self, member_id: str) -> List[Dict]:
        return library_repository.get_member_history(member_id)
    
    def get_members(self) -> List[Dict]:
        return library_repository.get_members()