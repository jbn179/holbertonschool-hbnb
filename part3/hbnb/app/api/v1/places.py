from flask_restx import Namespace, Resource, fields
from flask import request
from app.services.facade import facade  # Import facade instead of direct model
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity

# Changer Blueprint en Namespace
api = Namespace('places', description='Places operations')

# Définir le modèle pour la documentation
place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(description='Place description'),
    'price': fields.Float(required=True, description='Price per night'),
    'latitude': fields.Float(required=True, description='Latitude coordinate'),
    'longitude': fields.Float(required=True, description='Longitude coordinate'),
    'owner_id': fields.String(required=True, description='Owner ID')
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
                'user_id': place.user_id,
                'created_at': place.created_at.isoformat(),
                'updated_at': place.updated_at.isoformat()
            })
        return result, HTTPStatus.OK
    
    @api.doc('create_place')
    @api.expect(place_model)
    def post(self):
        """Create a new place without persisting relationships"""
        data = request.get_json()
        
        # Validate required fields
        required_fields = ['title', 'price', 'latitude', 'longitude', 'owner_id']
        for field in required_fields:
            if field not in data:
                return {'error': f'Missing required field: {field}'}, HTTPStatus.BAD_REQUEST
        
        try:
            # Use facade to create place
            new_place = facade.create_place(data)
            
            return {
                'id': new_place.id,
                'title': new_place.title,
                'description': new_place.description,
                'price': new_place.price,
                'latitude': new_place.latitude,
                'longitude': new_place.longitude,
                'user_id': new_place.user_id,
                'created_at': new_place.created_at.isoformat(),
                'updated_at': new_place.updated_at.isoformat()
            }, HTTPStatus.CREATED
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@api.route('/<string:place_id>')
@api.param('place_id', 'The place identifier')
class PlaceResource(Resource):
    @api.doc('get_place')
    def get(self, place_id):
        """Get a specific place"""
        place = facade.get_place(place_id)  # Use facade
        if not place:
            return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
            
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'user_id': place.user_id,
            'created_at': place.created_at.isoformat(),
            'updated_at': place.updated_at.isoformat()
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
        # Get current user from token
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        is_admin = current_user.get('is_admin', False)
        
        # Get place and check if it exists
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
        
        # Check ownership or admin status before allowing update
        if place.user_id != user_id and not is_admin:
            return {'error': 'You must be the owner or an admin to update this place'}, HTTPStatus.FORBIDDEN
            
        # Process the update (admins can update any place)
        try:
            place_data = api.payload
            updated_place = facade.update_place(place_id, place_data)
            
            # Return the updated place
            return {
                'id': updated_place.id,
                'name': updated_place.name,
                'description': updated_place.description,
                'user_id': updated_place.user_id,
                # Add other fields as needed
                'updated_at': updated_place.updated_at.isoformat()
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
    
    @api.doc('delete_place')
    @api.response(204, 'Place deleted successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Not the owner')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        """Delete a place (owner or admin only)"""
        # Get current user from token
        current_user = get_jwt_identity()
        user_id = current_user.get('id')
        is_admin = current_user.get('is_admin', False)
        
        # Get place and check if it exists
        place = facade.get_place_by_id(place_id)
        if not place:
            return {'error': 'Place not found'}, HTTPStatus.NOT_FOUND
        
        # Check ownership or admin status before allowing deletion
        if place.user_id != user_id and not is_admin:
            return {'error': 'You must be the owner or an admin to delete this place'}, HTTPStatus.FORBIDDEN
            
        # Delete the place (admins can delete any place)
        try:
            facade.delete_place(place_id)
            return '', HTTPStatus.NO_CONTENT
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
