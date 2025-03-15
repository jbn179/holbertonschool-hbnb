from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt
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
        credentials = api.payload
        if not credentials:
            return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
            
        email = credentials.get('email')
        password = credentials.get('password')
        
        if not email or not password:
            return {'error': 'Email and password are required'}, HTTPStatus.BAD_REQUEST
        
        # Retrieving user via facade
        try:
            user = facade.get_user_by_email(email)
            
            if not user:
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
            
            # Password verification
            if user.verify_password(password):
                # Creating JWT token
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={'is_admin': user.is_admin}
                )
                return {'access_token': access_token}, HTTPStatus.OK
            else:
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
                
        except Exception as e:
            return {'error': 'Authentication error'}, HTTPStatus.INTERNAL_SERVER_ERROR

@api.route('/profile')
class ProtectedUserProfile(Resource):
    @api.doc('protected_user_profile')
    @jwt_required()
    @api.response(200, 'User profile retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(404, 'User not found')
    def get(self):
        """A protected endpoint that returns the current user's profile"""
        user_id = get_jwt_identity()
        user = facade.get_user_by_id(user_id)
        
        if not user:
            return {'error': 'User not found'}, HTTPStatus.NOT_FOUND
            
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
    @jwt_required()
    @api.response(200, 'Admin content retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    @api.response(403, 'Forbidden - User is not an admin')
    def get(self):
        """An endpoint that only admins can access"""
        user_id = get_jwt_identity()
        claims = get_jwt()
        
        if not claims.get('is_admin', False):
            return {'error': 'Access denied: Admin privileges required'}, HTTPStatus.FORBIDDEN
            
        return {'message': 'Welcome, admin! Here is your secret content.'}, HTTPStatus.OK

@api.route('/protected')
class ProtectedResource(Resource):
    @api.doc('protected_resource')
    @jwt_required()
    @api.response(200, 'Protected content retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    def get(self):
        """A protected endpoint that requires authentication"""
        user_id = get_jwt_identity()
        return {'message': f'Hello! You are authenticated as user with ID: {user_id}'}, HTTPStatus.OK

# Endpoint for production tests - keep this
@api.route('/direct-login')
class DirectLogin(Resource):
    @api.doc('direct_login')
    @api.expect(login_model)
    def post(self):
        """Alternative login bypassing SQLAlchemy if needed"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')
        
        import sqlite3
        try:
            conn = sqlite3.connect('../instance/development.db')
            cursor = conn.cursor()
            
            cursor.execute("SELECT id, password, is_admin FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            
            if not user:
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
            
            user_id, password_hash, is_admin = user
                
            import bcrypt
            pw_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            
            result = bcrypt.checkpw(pw_bytes, hash_bytes)
            
            if result:
                access_token = create_access_token(
                    identity=str(user_id),
                    additional_claims={'is_admin': bool(is_admin)}
                )
                return {'access_token': access_token}, HTTPStatus.OK
            else:
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
        except Exception as e:
            return {'error': 'Authentication error'}, HTTPStatus.INTERNAL_SERVER_ERROR
        finally:
            if 'conn' in locals():
                conn.close()