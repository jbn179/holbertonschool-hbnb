from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_restx import Api
from flask_bcrypt import Bcrypt
from app import config

# Initialize bcrypt
bcrypt = Bcrypt()

# db instance
db = SQLAlchemy()

from app.api.v1.users import api as users_ns
from app.api.v1.amenities import api as amenities_ns
from app.api.v1.places import api as places_ns
from app.api.v1.reviews import api as reviews_ns
from app.api.v1.auth import api as auth_ns  # Ajout de l'import pour auth
from flask_jwt_extended import JWTManager

jwt = JWTManager()

def create_app(config_class=config.DevelopmentConfig):
    app = Flask(__name__)
    api = Api(app, version='1.0', title='HBnB API', description='HBnB Application API', doc='/api/v1/')
    jwt.init_app(app)
    
    # Configuration
    if config_class:
        app.config.from_object(config_class)
    else:
        app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///hbnb.db'
        app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    
    # Initialize extensions
    db.init_app(app)
    bcrypt.init_app(app)
    
    # Create tables
    with app.app_context():
        db.create_all()
    
    # Register blueprints and APIs
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')  # Ajout de l'enregistrement pour auth
    
    return app
