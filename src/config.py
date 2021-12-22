import os

from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv(raise_error_if_not_found=False))

POSTGRES_DB = os.getenv("POSTGRES_DB")
POSTGRES_USER = os.getenv("POSTGRES_USER")
POSTGRES_PASSWORD = os.getenv("POSTGRES_PASSWORD")
POSTGRES_HOST = os.getenv("POSTGRES_HOST")
POSTGRES_PORT = os.getenv("POSTGRES_PORT")

SQLALCHEMY_DATABASE_URI = f"postgresql://{POSTGRES_USER}:{POSTGRES_PASSWORD}@{POSTGRES_HOST}:{POSTGRES_PORT}/{POSTGRES_DB}"

SECRET_KEY = os.getenv("SECRET_KEY")
SALT = os.getenv("SALT")

SERVER_HOST = os.getenv("SERVER_HOST")
SERVER_PORT = int(os.getenv("SERVER_PORT"))
