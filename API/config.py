import os

class Config:
    SECRET_KEY = os.getenv("SECRET_KEY", "default_secret_key")
    DB_HOST = os.getenv("DB_HOST", "your_host")
    DB_USER = os.getenv("DB_USER", "your_user")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "your_password")
    DB_NAME = os.getenv("DB_NAME", "your_database")
    DB_CURSORCLASS = "DictCursor"
