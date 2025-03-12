from flask import Blueprint
from flask_restx import Api

# Create a blueprint for the API v1
api_bp = Blueprint('api', __name__, url_prefix='/api/v1')

# Initialize the Flask-RESTX API
api = Api(api_bp, 
    version='1.0',
    title='HBNB API',
    description='API for HBNB application'
)

# Import namespaces after creating the API
from .auth import api as auth_namespace
from .users import api as users_namespace
# Import other namespaces as needed

# Register namespaces with the API
api.add_namespace(auth_namespace, path='/auth')
api.add_namespace(users_namespace, path='/users')
# Register other namespaces as needed