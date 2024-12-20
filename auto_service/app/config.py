import os

class Config:
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:8527931@localhost/bd_cw'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    JWT_SECRET_KEY = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')
