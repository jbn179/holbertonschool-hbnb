from datetime import datetime
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services.facade import facade
from http import HTTPStatus
from flask import Blueprint, request, jsonify
from app.models.amenity import Amenity
from app import db
import uuid

api = Namespace('amenities', description='Amenity operations')

amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.expect(amenity_model, validate=True)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new amenity (admin only)"""
        # Check admin privileges
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        try:
            amenity_data = api.payload
            new_amenity = facade.create_amenity(amenity_data)
            return {
                'id': new_amenity.id,
                'name': new_amenity.name,
                'created_at': new_amenity.created_at.isoformat() if isinstance(new_amenity.created_at, datetime) else str(new_amenity.created_at),
                'updated_at': new_amenity.updated_at.isoformat() if isinstance(new_amenity.updated_at, datetime) else str(new_amenity.updated_at)
            }, HTTPStatus.CREATED
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """Get list of all amenities"""
        amenities = facade.get_all_amenities()
        return [{
            'id': amenity.id,
            'name': amenity.name,
            'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
            'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
        } for amenity in amenities], HTTPStatus.OK
        
@api.route('/<string:amenity_id>')
@api.param('amenity_id', 'The amenity identifier')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """Get amenity details by ID"""
        try:
            amenity = facade.get_amenity(amenity_id)
            if not amenity:
                return {'error': 'Amenity not found'}, HTTPStatus.NOT_FOUND
            return {
                'id': amenity.id,
                'name': amenity.name,
                'created_at': amenity.created_at.isoformat() if isinstance(amenity.created_at, datetime) else str(amenity.created_at),
                'updated_at': amenity.updated_at.isoformat() if isinstance(amenity.updated_at, datetime) else str(amenity.updated_at)
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.expect(amenity_model)
    @api.response(200, 'Amenity updated successfully')
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """Update amenity details (admin only)"""
        # Check admin privileges
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        try:
            amenity_data = api.payload
            updated_amenity = facade.update_amenity(amenity_id, amenity_data)
            if not updated_amenity:
                return {'error': 'Amenity not found'}, HTTPStatus.NOT_FOUND
            return {
                'id': updated_amenity.id,
                'name': updated_amenity.name,
                'created_at': updated_amenity.created_at.isoformat() if isinstance(updated_amenity.created_at, datetime) else str(updated_amenity.created_at),
                'updated_at': updated_amenity.updated_at.isoformat() if isinstance(updated_amenity.updated_at, datetime) else str(updated_amenity.updated_at)
            }, HTTPStatus.OK
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(204, 'Amenity deleted successfully')
    @api.response(404, 'Amenity not found')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - Admin privileges required')
    @jwt_required()
    def delete(self, amenity_id):
        """Delete an amenity (admin only)"""
        # Check admin privileges
        current_user = get_jwt_identity()
        if not current_user.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        try:
            result = facade.delete_amenity(amenity_id)
            if not result:
                return {'error': 'Amenity not found'}, HTTPStatus.NOT_FOUND
            return '', HTTPStatus.NO_CONTENT
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

amenities_bp = Blueprint('amenities', __name__)

@amenities_bp.route('/amenities', methods=['POST'])
@jwt_required()
def create_amenity():
    """Create a new amenity without persisting relationships (admin only)"""
    # Check admin privileges
    current_user = get_jwt_identity()
    if not current_user.get('is_admin', False):
        return jsonify({'error': 'Admin privileges required'}), 403
        
    data = request.get_json()
    
    # Validate required fields
    required_fields = ['name']
    for field in required_fields:
        if field not in data:
            return jsonify({'error': f'Missing required field: {field}'}), 400
    
    # Create a valid Amenity entity
    try:
        new_amenity = Amenity(
            id=str(uuid.uuid4()),
            name=data['name']
        )
        
        # Persist the amenity in database
        db.session.add(new_amenity)
        db.session.commit()
        
        return jsonify({
            'id': new_amenity.id,
            'name': new_amenity.name,
            'created_at': new_amenity.created_at.isoformat(),
            'updated_at': new_amenity.updated_at.isoformat()
        }), 201
        
    except ValueError as e:
        return jsonify({'error': str(e)}), 400
