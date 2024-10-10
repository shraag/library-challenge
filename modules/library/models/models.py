from enum import Enum

class UserRoles(Enum):
    LIBRARIAN = 'LIBRARIAN'
    MEMBER = 'MEMBER'

class UserStatus(Enum):
    ACTIVE = 'ACTIVE'
    DELETED = 'DELETED'

class BookStatus(Enum):
    AVAILABLE = 'AVAILABLE'
    BORROWED = 'BORROWED'
class Action(Enum):
    BORROWED = 'BORROWED'
    RETURNED = 'RETURNED'