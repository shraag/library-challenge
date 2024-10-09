import os
from dotenv import load_dotenv

load_dotenv('.env')
class Config:
    SECRET_KEY = os.environ.get("SECRET_KEY")
    SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:8july2001@localhost/library_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    URL_BASE_PATH = os.getenv('URL_BASE_PATH', '')
    JWT_EXPIRATION_MINUTES = os.getenv('JWT_EXPIRATION_MINUTES', 15)
