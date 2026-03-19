import os

class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY') or 'secret-key'
    SQLALCHEMY_DATABASE_URI = "postgresql://missytina22:lab4user@localhost/lab4"
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    
    UPLOAD_FOLDER = os.path.join("app", "static", "uploads")