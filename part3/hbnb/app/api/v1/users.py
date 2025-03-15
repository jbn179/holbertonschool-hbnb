from flask_restx import Namespace, Resource, fields
from flask import request
from http import HTTPStatus
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt  # Add this import
from app.services.facade import facade
from datetime import datetime

api = Namespace('users', description='User operations')

# Update the user model to include a password field
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Admin user creation/update model
admin_user_model = api.model('AdminUserModel', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password'),
    'is_admin': fields.Boolean(required=False, description='Admin status')
})

# Create a response model that doesn't include the password
user_response_model = api.model('UserResponse', {
    'id': fields.String(description='User ID'),
    'first_name': fields.String(description='User first name'),
    'last_name': fields.String(description='User last name'),
    'email': fields.String(description='User email')
})

# Registration success response model
registration_response = api.model('RegistrationResponse', {
    'id': fields.String(description='User ID'),
    'message': fields.String(description='Success message')
})

@api.route('/')
class UserList(Resource):
    @api.doc('create_user')
    @api.expect(user_model)
    @api.response(201, 'User created successfully', registration_response)
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Register a new user (admin only)"""
        # Check administrator privileges
        user_id = get_jwt_identity()  # Now just the ID
        claims = get_jwt()  # Retrieve additional claims
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        data = request.json
        
        # Validate required fields
        if not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
            return {'message': 'Missing required fields'}, HTTPStatus.BAD_REQUEST
        
        # Ensure minimum password complexity
        if len(data.get('password', '')) < 8:
            return {'message': 'Password must be at least 8 characters long'}, HTTPStatus.BAD_REQUEST
        
        # Verify if email is already registered
        if facade.get_user_by_email(data.get('email')):
            return {'message': 'Email already registered'}, HTTPStatus.BAD_REQUEST
        
        try:
            # Create the user - password will be hashed by the User model
            user = facade.create_user(data)
            
            # Return only ID and success message, not the password
            return {
                'id': user.id,
                'message': 'User registered successfully'
            }, HTTPStatus.CREATED
        
        except ValueError as e:
            return {'message': str(e)}, HTTPStatus.BAD_REQUEST

    @api.response(200, 'List of users retrieved successfully')
    def get(self):
        """Get list of all users"""
        users = facade.get_all_users()
        return [{
            'id': user.id, 
            'first_name': user.first_name, 
            'last_name': user.last_name, 
            'email': user.email,
            'created_at': user.created_at.isoformat() if isinstance(user.created_at, datetime) else str(user.created_at),
            'updated_at': user.updated_at.isoformat() if isinstance(user.updated_at, datetime) else str(user.updated_at)
        } for user in users], 200

@api.route('/<string:user_id>')
@api.param('user_id', 'The user identifier')
class UserResource(Resource):
    @api.doc('get_user')
    @api.response(200, 'Success', user_response_model)
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get a user by ID"""
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, HTTPStatus.OK

    @api.doc('update_user')
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Admin privileges required')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update a user (admin only)"""
        # check admin 
        current_user_id = get_jwt_identity()  # Renommez cette variable
        claims = get_jwt()  # Retrieve additional claims
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
        
        # Get the user to update
        user = facade.get_user_by_id(user_id)  # Maintenant utilise l'ID de l'URL
        if not user:
            return {'error': 'User not found'}, HTTPStatus.NOT_FOUND
        
        # Get the update data
        data = request.json
        email = data.get('email')
        
        # Ensure email uniqueness if changing email
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, HTTPStatus.BAD_REQUEST
                
        try:
            # Update user with all data, including email and password if provided
            facade.update_user(user_id, data)
            updated_user = facade.get_user_by_id(user_id)
            
            # Return the updated user (without password)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat() if isinstance(updated_user.created_at, datetime) else str(updated_user.created_at),
                'updated_at': updated_user.updated_at.isoformat() if isinstance(updated_user.updated_at, datetime) else str(updated_user.updated_at)
            }, HTTPStatus.OK
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@api.route('/admin')
class AdminUserManagement(Resource):
    @api.doc('admin_create_user')
    @api.expect(admin_user_model)
    @api.response(201, 'User created successfully by admin', registration_response)
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Admin creates a new user (admin only)"""
        # Check admin privileges
        user_id = get_jwt_identity()  # Now just the ID
        claims = get_jwt()  # Retrieve additional claims
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
        
        data = request.json
        email = data.get('email')
        
        # Validate required fields
        if not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
            return {'error': 'Missing required fields'}, HTTPStatus.BAD_REQUEST
            
        # Check if email is already in use
        if facade.get_user_by_email(email):
            return {'error': 'Email already registered'}, HTTPStatus.BAD_REQUEST
            
        try:
            # Create user with admin flag if specified
            user = facade.create_user(data)
            
            return {
                'id': user.id,
                'message': 'User created successfully by admin'
            }, HTTPStatus.CREATED
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST

@api.route('/<string:user_id>/admin')
@api.param('user_id', 'The user identifier')
class AdminUserModify(Resource):
    @api.doc('admin_update_user')
    @api.expect(user_model)
    @jwt_required()
    def put(self, user_id):
        """Admin updates a user (admin only, can update email and password)"""
        # Check admin privileges
        current_user_id = get_jwt_identity()  # Renommer cette variable
        claims = get_jwt()  # Retrieve additional claims
        if not claims.get('is_admin', False):
            return {'error': 'Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        # Get the user to update - maintenant utilise correctement user_id de l'URL
        user = facade.get_user_by_id(user_id)
        if not user:
            return {'error': 'User not found'}, HTTPStatus.NOT_FOUND
        
        # Get the update data
        data = request.json
        email = data.get('email')
        
        # Ensure email uniqueness if changing email
        if email:
            existing_user = facade.get_user_by_email(email)
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, HTTPStatus.BAD_REQUEST
                
        try:
            # Update user with all data, including email and password
            facade.update_user(user_id, data)
            updated_user = facade.get_user_by_id(user_id)
            
            # Return the updated user (without password)
            return {
                'id': updated_user.id,
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name,
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat() if isinstance(updated_user.created_at, datetime) else str(updated_user.created_at),
                'updated_at': updated_user.updated_at.isoformat() if isinstance(updated_user.updated_at, datetime) else str(updated_user.updated_at)
            }, HTTPStatus.OK
            
        except ValueError as e:
            return {'error': str(e)}, HTTPStatus.BAD_REQUEST
