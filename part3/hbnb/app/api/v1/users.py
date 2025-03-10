from datetime import datetime
from flask import request
from flask_restx import Namespace, Resource, fields
from app.services.facade import facade
from http import HTTPStatus

api = Namespace('users', description='User operations')

# Update the user model to include a password field
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='User first name'),
    'last_name': fields.String(required=True, description='User last name'),
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
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
    def post(self):
        """Register a new user"""
        data = request.json
        
        # Validate required fields
        if not all(key in data for key in ['first_name', 'last_name', 'email', 'password']):
            return {'message': 'Missing required fields'}, HTTPStatus.BAD_REQUEST
        
        try:
            # Create user - password will be hashed by the User model
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
        user = facade.get_user(user_id)
        if not user:
            return {'message': 'User not found'}, HTTPStatus.NOT_FOUND
        
        # Return user data without password
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email
        }, HTTPStatus.OK

            
    @api.expect(user_model)
    @api.response(200, 'User updated successfully')
    @api.response(404, 'User not found')
    @api.response(400, 'Invalid input data')
    def put(self, user_id):
        """Update user details"""
        try:
            user_data = api.payload
            updated_user = facade.update_user(user_id, user_data)
            if not updated_user:
                return {'error': 'User not found'}, 404
            return {
                'id': updated_user.id, 
                'first_name': updated_user.first_name,
                'last_name': updated_user.last_name, 
                'email': updated_user.email,
                'is_admin': updated_user.is_admin,
                'created_at': updated_user.created_at.isoformat() if isinstance(updated_user.created_at, datetime) else str(updated_user.created_at),
                'updated_at': updated_user.updated_at.isoformat() if isinstance(updated_user.updated_at, datetime) else str(updated_user.updated_at)
            }, 200
        except ValueError as e:
            return {'error': str(e)}, 400

