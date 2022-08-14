import os
from dotenv import load_dotenv
from datetime import timedelta

basedir = os.path.abspath(os.path.dirname(__file__))
load_dotenv(os.path.join(basedir, '.env'))


class Config:
    JWT_SECRET_KEY = os.environ.get("JWT_SECRET_KEY")
    JWT_AUTH_USERNAME_KEY = "username"
    JWT_AUTH_PASSWORD_KEY = "password"
    JWT_ACCESS_TOKEN_EXPIRES = timedelta(minutes=10)
    JWT_REFRESH_TOKEN_EXPIRES = timedelta(days=30)
    PROPAGATE_EXCEPTIONS = True


class ProdConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///prod_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = True


class DevConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///dev_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False


class TestConfig:
    SQLALCHEMY_DATABASE_URI = 'sqlite:///test_data.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
