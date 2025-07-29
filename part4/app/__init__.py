from flask import Flask
from flask_restx import Api
from flask_cors import CORS

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns

from config import DevelopmentConfig

from app.extensions import bcrypt
from app.extensions import jwt
from app.extensions import db
from app.services import facade

def seed_admin_user(app):
    with app.app_context():
        email = app.config['ADMIN_EMAIL']
        password = app.config['ADMIN_PASSWORD']
        first_name = app.config['ADMIN_FIRST_NAME']
        last_name = app.config['ADMIN_LAST_NAME']

        existing_user = facade.get_user_by_email(email)
        if not existing_user:
            facade.create_user({
                "first_name": first_name,
                "last_name": last_name,
                "email": email,
                "password": password,
                "is_admin": True
            })


def create_app(config_class=DevelopmentConfig):
    app = Flask(__name__)
    app.config.from_object(config_class)

    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    CORS(app)

    with app.app_context():
        db.create_all()
        seed_admin_user(app)

    # This is for not to curl everything
    # Swagger Authorizations
    api = Api(
        app,
        version=app.config['RESTX_VERSION'],
        title=app.config['RESTX_TITLE'],
        description=app.config['RESTX_DESCRIPTION'],
        doc=app.config['RESTX_DOC'],
        authorizations=app.config['RESTX_AUTHORIZE'],
        security=app.config['RESTX_SECURITY']
    )

    # Register the users namespace
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    return app
