from flask import Blueprint

# Corriger l'importation - utiliser api au lieu de places_bp
from app.api.v1.places import api as places_api
from app.api.v1.users import api as users_api

api_bp = Blueprint('api', __name__)

# Si vous avez besoin d'enregistrer ces blueprints/namespaces
# Mais ce n'est probablement pas nécessaire car ils sont déjà enregistrés dans app/__init__.py