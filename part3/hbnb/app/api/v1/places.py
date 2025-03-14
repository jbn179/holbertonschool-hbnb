from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Ajouter get_jwt ici
from app.services.facade import facade
from http import HTTPStatus
from flask import Blueprint, request, jsonify

# Changer Blueprint en Namespace
api = Namespace('places', description='Places operations')

# Modifier le modèle pour utiliser owner_id au lieu de user_id
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='Owner ID'),  # Utilise owner_id au lieu de user_id
    'amenities': fields.List(fields.String, description='List of amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.doc('list_places')
    def get(self):
        """Get all places"""
        places = facade.get_all_places()  # Use facade instead of direct query
        result = []
        for place in places:
            result.append({
                'id': place.id,
                'title': place.title,
                'description': place.description,
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'owner_id': place.user_id,  # Utiliser owner_id au lieu de user_id pour cohérence
                'created_at': place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
                'updated_at': place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
            })
        return result, HTTPStatus.OK
    
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @jwt_required()
    def post(self):
        """Create a new place"""
        try:
            # Get current user from token
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            
            data = request.json
            
            # Vérifier si l'utilisateur est le propriétaire ou un admin
            if not claims.get('is_admin', False) and data.get('owner_id') != current_user_id:
                return {'error': 'You can only create places for yourself unless you are an admin'}, HTTPStatus.FORBIDDEN
                
            # Traiter les amenities séparément si nécessaire
            amenities = data.pop('amenities', []) if 'amenities' in data else []
            
            # Convertir owner_id en user_id pour le modèle
            data_for_model = data.copy()
            if 'owner_id' in data_for_model:
                data_for_model['user_id'] = data_for_model.pop('owner_id')
            
            # S'assurer que les amenities sont incluses
            data_for_model['amenities'] = amenities
                
            # Créer la place
            place = facade.create_place(data_for_model)
            
            # Répondre avec les données de la place créée en utilisant owner_id pour l'API
            response = {
                'id': place.id, 
                'title': place.title,
                'description': place.description,
                'owner_id': place.user_id,  # Mapper user_id à owner_id pour la réponse
                'price': place.price,
                'latitude': place.latitude,
                'longitude': place.longitude,
                'created_at': place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
                'updated_at': place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
            }
            
            return response, HTTPStatus.CREATED
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f"An unexpected error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get a specific place"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner_id': place.user_id,
            'amenities': [{'id': amenity.id, 'name': amenity.name} for amenity in place.amenities],
            'created_at': place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
            'updated_at': place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
        }, HTTPStatus.OK
    
    @api.doc('update_place')
    @api.expect(place_model)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the owner')
    @api.response(404, 'Place not found')
    @jwt_required()
    def put(self, place_id):
        """Update place details (owner or admin only)"""
        try:
            # Get current user from token
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            is_admin = claims.get('is_admin', False)
            
            # Get place and check if it exists
            place = facade.get_place_by_id(place_id)
            if not place:
                return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
            
            # Check ownership or admin status before allowing update
            if place.user_id != current_user_id and not is_admin:
                return {'error': 'You must be the owner or an admin to update this place'}, HTTPStatus.FORBIDDEN
                
            # Convertir owner_id en user_id pour le modèle si présent
            place_data = request.json.copy()
            if 'owner_id' in place_data:
                place_data['user_id'] = place_data.pop('owner_id')
                
            # Process the update (admins can update any place)
            updated_place = facade.update_place(place_id, place_data)
            
            # Return the updated place with consistent field naming
            return {
                'id': updated_place.id,
                'title': updated_place.title,  # Utiliser title au lieu de name
                'description': updated_place.description,
                'owner_id': updated_place.user_id,  # Convertir user_id en owner_id pour l'API
                'price': updated_place.price,
                'latitude': updated_place.latitude,
                'longitude': updated_place.longitude,
                'created_at': updated_place.created_at.isoformat() if isinstance(updated_place.created_at, datetime) else str(updated_place.created_at),
                'updated_at': updated_place.updated_at.isoformat() if isinstance(updated_place.updated_at, datetime) else str(updated_place.updated_at)
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f"An unexpected error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc('delete_place')
    @api.response(204, 'Place deleted successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the owner')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (owner or admin only)"""
        try:
            # Get current user from token
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            is_admin = claims.get('is_admin', False)
            
            # Get place and check if it exists
            place = facade.get_place_by_id(place_id)
            if not place:
                return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
            
            # Check ownership or admin status before allowing deletion
            if place.user_id != current_user_id and not is_admin:
                return {'error': 'You must be the owner or an admin to delete this place'}, HTTPStatus.FORBIDDEN
                
            # Delete the place (admins can delete any place)
            facade.delete_place(place_id)
            return '', HTTPStatus.NO_CONTENT
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f"An unexpected error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/<string:place_id>/amenities')
@api.param('place_id', 'The place identifier')
class PlaceAmenities(Resource):
    @api.doc('get_place_amenities')
    def get(self, place_id):
        """Get place with its amenities"""
        try:
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
                
            # Récupérer les détails du propriétaire avec gestion d'attributs manquants
            owner_details = None
            try:
                owner = facade.get_user_by_id(place.user_id) if place.user_id else None
                if owner:
                    owner_details = {
                        'id': owner.id,
                        # Utilise getattr avec des valeurs par défaut pour éviter les AttributeError
                        'email': getattr(owner, 'email', None),
                        'first_name': getattr(owner, 'first_name', None),
                        'last_name': getattr(owner, 'last_name', None)
                        # Ne pas utiliser username s'il n'existe pas
                    }
            except Exception as e:
                print(f"Erreur lors de la récupération du propriétaire: {str(e)}")
                owner_details = {'id': place.user_id, 'error': 'Owner details not available'}
            
            # Récupérer les amenities avec gestion d'erreur
            amenities_details = []
            if hasattr(place, 'amenities'):
                for amenity in place.amenities:
                    try:
                        amenities_details.append({
                            'id': amenity.id,
                            'name': getattr(amenity, 'name', 'Unknown'),
                            'created_at': str(getattr(amenity, 'created_at', '')),
                            'updated_at': str(getattr(amenity, 'updated_at', ''))
                        })
                    except Exception as e:
                        print(f"Erreur lors de la récupération d'une amenity: {str(e)}")
            
            # Construire une réponse détaillée
            response = {
                'place': {
                    'id': place.id,
                    'title': getattr(place, 'title', None),
                    'description': getattr(place, 'description', None),
                    'price': getattr(place, 'price', None),
                    'latitude': getattr(place, 'latitude', None),
                    'longitude': getattr(place, 'longitude', None),
                    'owner': owner_details,
                    'created_at': str(getattr(place, 'created_at', '')),
                    'updated_at': str(getattr(place, 'updated_at', ''))
                },
                'amenities': amenities_details,
                'total_amenities': len(amenities_details)
            }
                
            return response, HTTPStatus.OK
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f"An unexpected error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
    
    @api.doc('update_place_amenities')
    @api.expect(api.model('PlaceAmenities', {
        'amenities': fields.List(fields.String, required=True, description='List of amenity IDs')
    }))
    @jwt_required()
    def put(self, place_id):
        """Update amenities of a place (owner or admin only)"""
        try:
            # Get current user from token
            claims = get_jwt()
            current_user_id = get_jwt_identity()
            is_admin = claims.get('is_admin', False)
            
            # Get place and check if it exists
            place = facade.get_place(place_id)
            if not place:
                return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
            
            # Check ownership or admin status before allowing update
            if place.user_id != current_user_id and not is_admin:
                return {'error': 'You must be the owner or an admin to update this place'}, HTTPStatus.FORBIDDEN
            
            # Update amenities
            amenities_data = request.json.get('amenities', [])
            place_data = {'amenities': amenities_data}
            updated_place = facade.update_place(place_id, place_data)
            
            # Format response
            amenities_details = [
                {
                    'id': amenity.id,
                    'name': amenity.name,
                    'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
                    'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
                } for amenity in updated_place.amenities
            ]
            
            response = {
                'place': {
                    'id': updated_place.id,
                    'title': updated_place.title,
                    'description': updated_place.description,
                    'price': updated_place.price,
                    'latitude': updated_place.latitude,
                    'longitude': updated_place.longitude,
                    'owner_id': updated_place.user_id,
                    'created_at': updated_place.created_at.isoformat() if isinstance(updated_place.created_at, datetime) else str(updated_place.created_at),
                    'updated_at': updated_place.updated_at.isoformat() if isinstance(updated_place.updated_at, datetime) else str(updated_place.updated_at)
                },
                'amenities': amenities_details,
                'total_amenities': len(amenities_details)
            }
            
            return response, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
        except Exception as e:
            import traceback
            traceback.print_exc()
            return {'error': f"An unexpected error occurred: {str(e)}"}, HTTPStatus.INTERNAL_SERVER_ERROR
