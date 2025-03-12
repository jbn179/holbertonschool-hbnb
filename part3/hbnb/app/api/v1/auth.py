from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from app.services.facade import facade
from http import HTTPStatus

api = Namespace('auth', description='Authentication operations')

# Model for login input validation
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

# Model for successful login response
token_model = api.model('Token', {
    'access_token': fields.String(description='JWT access token')
})

@api.route('/login')
class Login(Resource):
    @api.doc('user_login')
    @api.expect(login_model)
    @api.response(200, 'Login successful', token_model)
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT token"""
        credentials = api.payload  # Get the email and password from the request payload
        
        # Step 1: Retrieve the user based on the provided email
        user = facade.get_user_by_email(credentials['email'])
        
        # Step 2: Check if the user exists and the password is correct
        if not user or not user.verify_password(credentials['password']):
            return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED

        # Step 3: Create a JWT token with the user's id and is_admin flag
        access_token = create_access_token(identity={'id': str(user.id), 'is_admin': user.is_admin})
        
        # Step 4: Return the JWT token to the client
        return {'access_token': access_token}, HTTPStatus.OK

@api.route('/profile')
class ProtectedUserProfile(Resource):
    @api.doc('protected_user_profile')
    @jwt_required()  # This endpoint requires a valid JWT token
    @api.response(200, 'User profile retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    def get(self):
        """A protected endpoint that returns the current user's profile"""
        # Get the identity from the JWT token
        current_user = get_jwt_identity()
        
        # Retrieve the user from the database
        user = facade.get_user_by_id(current_user['id'])
        
        if not user:
            return {'error': 'User not found'}, HTTPStatus.NOT_FOUND
            
        # Return the user profile
        return {
            'id': user.id,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'email': user.email,
            'is_admin': user.is_admin
        }, HTTPStatus.OK

@api.route('/admin-only')
class AdminOnlyResource(Resource):
    @api.doc('admin_only_resource')
    @jwt_required()  # This endpoint requires a valid JWT token
    @api.response(200, 'Admin content retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - User is not an admin')
    def get(self):
        """An endpoint that only admins can access"""
        # Get the identity from the JWT token
        current_user = get_jwt_identity()
        
        # Check if the user is an admin
        if not current_user.get('is_admin', False):
            return {'error': 'Access denied: Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        # Return admin-only content
        return {'message': 'Welcome, admin! Here is your secret content.'}, HTTPStatus.OK