import os

class Config:
    SECRET_KEY = os.getenv('SECRET_KEY', 'default_secret_key')
    DEBUG = False

    # Vars to seed the Admin user
    ADMIN_EMAIL = os.getenv('ADMIN_EMAIL', 'admin@hbnb.com')
    ADMIN_PASSWORD = os.getenv('ADMIN_PASSWORD', 'string')
    ADMIN_FIRST_NAME = os.getenv('ADMIN_FIRST_NAME', 'Admin')
    ADMIN_LAST_NAME = os.getenv('ADMIN_LAST_NAME', 'User')

    # Vars to Swagger Authorizations
    RESTX_AUTHORIZE = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Paste your JWT token here with **Bearer <your_token>**'
        }
    }

    RESTX_TITLE = 'HBnB API'
    RESTX_VERSION = '1.0'
    RESTX_DESCRIPTION = 'HBnB Application API'
    RESTX_DOC = '/'
    RESTX_SECURITY = 'Bearer Auth'

class DevelopmentConfig(Config):
    DEBUG = True
    SQLALCHEMY_DATABASE_URI = 'sqlite:///development.db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False

config = {
    'development': DevelopmentConfig,
    'default': DevelopmentConfig
}