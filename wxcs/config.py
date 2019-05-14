"""Application configuration.

Most configuration is set via environment variables.

For local development, use a .env file to set
environment variables.
"""
from environs import Env

env = Env()
env.read_env()

ENV = env.str('FLASK_ENV', default='production')
DEBUG = (ENV == 'development')
SECRET_KEY = env.str('SECRET_KEY')
SQLALCHEMY_DATABASE_URI = env.str('DATABASE_URL')
SQLALCHEMY_TRACK_MODIFICATIONS = False
BCRYPT_LOG_ROUNDS = env.int('BCRYPT_LOG_ROUNDS', default=13)
