import os

class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY") or "your_secret_key"
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:8july2001@localhost/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY") or "your_jwt_secret_key"
    # URL_BASE_PATH = os.getenv('URL_BASE_PATH', '')
    URL_BASE_PATH = '/api'
