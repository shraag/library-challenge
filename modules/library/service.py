from modules.library.repository.repository import LibraryRepository
from modules.library.models.requests import SignUpRequest
from modules.library.repository.models import User

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