#!/usr/bin/python3
from flask import Flask
from flask_restx import Api
from app.api.v1.reviews import api as reviews_namesapce

def create_app():
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')

    api.add_namespace(reviews_namesapce, path='/reviews')
    # Additional namespaces for places, reviews, and amenities will be added later

    return app