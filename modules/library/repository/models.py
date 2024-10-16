from app import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    first_name = db.Column(db.String(255), nullable=False)
    last_name = db.Column(db.String(255), nullable=False)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.Enum('LIBRARIAN', 'MEMBER'), nullable=False)
    status = db.Column(db.Enum('ACTIVE', 'DELETED'), default='ACTIVE')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "username": self.username,
            "status": self.status
        }

class Book(db.Model):
    __tablename__ = 'books'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    title = db.Column(db.String(255), nullable=False)
    author = db.Column(db.String(255), nullable=True)
    published_year = db.Column(db.String(4))
    status = db.Column(db.Enum('AVAILABLE', 'BORROWED'), default='AVAILABLE')
    created_at = db.Column(db.DateTime, default=datetime.now)
    updated_at = db.Column(db.DateTime, default=datetime.now, onupdate=datetime.now)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}

class MemberHistory(db.Model):
    __tablename__ = 'member_history'

    id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    member_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='CASCADE'), nullable=False)
    book_id = db.Column(db.Integer, db.ForeignKey('books.id', ondelete='CASCADE'), nullable=False)
    action = db.Column(db.Enum('BORROWED', 'RETURNED'), nullable=False)
    action_date = db.Column(db.DateTime, default=datetime.now)

    def to_dict(self):
        return {column.name: getattr(self, column.name) for column in self.__table__.columns}