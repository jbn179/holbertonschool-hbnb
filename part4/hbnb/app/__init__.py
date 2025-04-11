from flask import Flask, request, jsonify
from flask_restx import Api
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_sqlalchemy import SQLAlchemy
from datetime import timedelta
from flask_cors import CORS

# Définir les extensions en premier
bcrypt = Bcrypt()
jwt = JWTManager()
db = SQLAlchemy()

def create_app(config_class="config.DevelopmentConfig"):
    app = Flask(__name__)
    app.config.from_object(config_class)
    
    # Désactiver la gestion automatique de CORS pour éviter les doublons et les conflits
    app.config['CORS_ENABLED'] = False
    
    # Gérer manuellement les requêtes preflight OPTIONS
    @app.before_request
    def handle_preflight():
        if request.method == 'OPTIONS':
            headers = {
                'Access-Control-Allow-Origin': 'http://localhost:8080',
                'Access-Control-Allow-Methods': 'GET, POST, PUT, DELETE, OPTIONS',
                'Access-Control-Allow-Headers': 'Content-Type, Authorization, Accept',
                'Access-Control-Allow-Credentials': 'true',
                'Access-Control-Max-Age': '3600',
                'Vary': 'Origin'
            }
            return ('', 204, headers)  # Répondre directement, pas de redirection
    
    # Ajouter manuellement les en-têtes CORS à toutes les réponses
    @app.after_request
    def add_cors_headers(response):
        response.headers.set('Access-Control-Allow-Origin', 'http://localhost:8080')
        response.headers.set('Access-Control-Allow-Methods', 'GET, POST, PUT, DELETE, OPTIONS')
        response.headers.set('Access-Control-Allow-Headers', 'Content-Type, Authorization, Accept')
        response.headers.set('Access-Control-Allow-Credentials', 'true')
        response.headers.set('Access-Control-Max-Age', '3600')
        response.headers.set('Vary', 'Origin')
        return response
    
    # Set JWT configuration
    app.config['JWT_JSON_SERIALIZATION_ENABLED'] = True
    app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=24)  # Tokens valides pendant 24h
    
    # Initialize extensions
    bcrypt.init_app(app)
    jwt.init_app(app)
    db.init_app(app)
    
    # Créer l'API Flask-RestX
    authorizations = {
        'Bearer Auth': {
            'type': 'apiKey',
            'in': 'header',
            'name': 'Authorization',
            'description': 'Add a JWT token to the header with the format: Bearer <JWT_TOKEN>'
        }
    }
    
    api = Api(app, 
              version='1.0', 
              title='HBnB API', 
              description='HBnB Application API', 
              doc='/api/v1/',
              authorizations=authorizations,
              security='Bearer Auth')
    
    # Importer les namespaces APRÈS avoir initialisé db
    # Ces importations sont déplacées ici pour éviter les importations circulaires
    from app.api.v1.users import api as users_ns
    from app.api.v1.amenities import api as amenities_ns
    from app.api.v1.places import api as places_ns
    from app.api.v1.reviews import api as reviews_ns
    from app.api.v1.auth import api as auth_ns
    
    # Register the namespaces
    api.add_namespace(users_ns, path='/api/v1/users')
    api.add_namespace(amenities_ns, path='/api/v1/amenities')
    api.add_namespace(places_ns, path='/api/v1/places')
    api.add_namespace(reviews_ns, path='/api/v1/reviews')
    api.add_namespace(auth_ns, path='/api/v1/auth')
    
    return app
