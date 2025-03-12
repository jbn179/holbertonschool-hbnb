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
        # Import façade
        from app.services.facade import facade
        
        # Débogage
        print("\n==== LOGIN ATTEMPT ====")
        
        # Validation des données d'entrée
        credentials = api.payload
        if not credentials:
            return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
            
        email = credentials.get('email')
        password = credentials.get('password')
        
        if not email or not password:
            return {'error': 'Email and password are required'}, HTTPStatus.BAD_REQUEST
        
        # Récupération de l'utilisateur via la façade (respecte l'architecture)
        try:
            user = facade.get_user_by_email(email)
            print(f"User found: {user is not None}")
            
            if not user:
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
            
            # Débogage
            print(f"Verifying password for {email}")
            
            # Vérification du mot de passe
            if user.verify_password(password):
                # Création du token JWT
                from flask_jwt_extended import create_access_token
                access_token = create_access_token(
                    identity=str(user.id),
                    additional_claims={'is_admin': user.is_admin}
                )
                return {'access_token': access_token}, HTTPStatus.OK
            else:
                print("Password verification failed")
                return {'error': 'Invalid credentials'}, HTTPStatus.UNAUTHORIZED
                
        except Exception as e:
            print(f"Error during login: {str(e)}")
            import traceback
            traceback.print_exc()
            return {'error': 'Authentication error'}, HTTPStatus.INTERNAL_SERVER_ERROR

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

@api.route('/protected')
class ProtectedResource(Resource):
    @api.doc('protected_resource')
    @jwt_required()  # This endpoint requires a valid JWT token
    @api.response(200, 'Protected content retrieved successfully')
    @api.response(401, 'Unauthorized - Missing or invalid token')
    def get(self):
        """A protected endpoint that requires authentication"""
        # Get the identity from the JWT token
        current_user = get_jwt_identity()
        
        # Return some protected content
        return {'message': f'Hello! You are authenticated as user with ID: {current_user["id"]}'}, HTTPStatus.OK

@api.route('/test-auth')
class TestAuth(Resource):
    @api.doc('test_auth')
    @api.expect(login_model)
    def post(self):
        """Test authentication directly"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')
        
        # Get user
        user = facade.get_user_by_email(email)
        if not user:
            return {'result': False, 'error': 'User not found'}, 200
        
        # Test methods
        results = {
            'user_found': True,
            'user_id': str(user.id),
            'email': user.email
        }
        
        # Test verify_password method
        try:
            method_result = user.verify_password(password)
            results['verify_password_method'] = method_result
        except Exception as e:
            results['verify_password_error'] = str(e)
        
        # Test direct bcrypt verification
        try:
            import bcrypt
            pw_bytes = password.encode('utf-8')
            hash_bytes = user.password.encode('utf-8')
            direct_result = bcrypt.checkpw(pw_bytes, hash_bytes)
            results['direct_bcrypt_verification'] = direct_result
        except Exception as e:
            results['direct_bcrypt_error'] = str(e)
            
        return results, 200

@api.route('/direct-login')
class DirectLogin(Resource):
    @api.doc('direct_login')
    @api.expect(login_model)
    def post(self):
        """Test direct login bypassing SQLAlchemy"""
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')
        
        # Utiliser SQLite directement
        import sqlite3
        try:
            conn = sqlite3.connect('../instance/development.db')
            cursor = conn.cursor()
            
            # Récupérer l'utilisateur directement
            cursor.execute("SELECT id, password, is_admin FROM users WHERE email=?", (email,))
            user = cursor.fetchone()
            
            if not user:
                return {'result': 'User not found'}, 200
            
            user_id, password_hash, is_admin = user
                
            # Tester le mot de passe directement
            import bcrypt
            pw_bytes = password.encode('utf-8')
            hash_bytes = password_hash.encode('utf-8')
            
            result = bcrypt.checkpw(pw_bytes, hash_bytes)
            
            if result:
                from flask_jwt_extended import create_access_token
                access_token = create_access_token(
                    identity=str(user_id),
                    additional_claims={'is_admin': bool(is_admin)}
                )
                return {
                    'result': 'Authentication successful', 
                    'user_id': user_id,
                    'access_token': access_token
                }, 200
            else:
                return {'result': 'Password incorrect'}, 200
        except Exception as e:
            return {'error': str(e)}, 500
        finally:
            if 'conn' in locals():
                conn.close()

@api.route('/debug-auth')
class DebugAuth(Resource):
    @api.doc('debug_auth')
    @api.expect(login_model)
    def post(self):
        """Debug authentication flow"""
        results = {}
        credentials = api.payload
        email = credentials.get('email')
        password = credentials.get('password')
        
        # Test 1: Import direct
        try:
            results["test1"] = {"name": "Direct import test"}
            from app.models.user import User
            results["test1"]["success"] = True
        except Exception as e:
            results["test1"]["success"] = False
            results["test1"]["error"] = str(e)
        
        # Test 2: Facade get_user_by_email
        try:
            results["test2"] = {"name": "Facade get_user_by_email"}
            from app.services.facade import facade
            user = facade.get_user_by_email(email)
            results["test2"]["success"] = user is not None
            if user:
                results["test2"]["user_id"] = str(user.id)
                results["test2"]["email"] = user.email
        except Exception as e:
            results["test2"]["success"] = False
            results["test2"]["error"] = str(e)
            
        # Test 3: Repository get_user_by_email
        try:
            results["test3"] = {"name": "Repository get_user_by_email"}
            from app.persistence.user_repository import UserRepository
            repo = UserRepository()
            user = repo.get_user_by_email(email)
            results["test3"]["success"] = user is not None
            if user:
                results["test3"]["user_id"] = str(user.id)
        except Exception as e:
            results["test3"]["success"] = False
            results["test3"]["error"] = str(e)
            
        # Test 4: User.verify_password
        if "test2" in results and results["test2"].get("success"):
            try:
                results["test4"] = {"name": "User.verify_password"}
                user = facade.get_user_by_email(email)
                result = user.verify_password(password)
                results["test4"]["success"] = result
                results["test4"]["password_verified"] = result
            except Exception as e:
                results["test4"]["success"] = False
                results["test4"]["error"] = str(e)
                
        # Test 5: Direct bcrypt check
        if "test2" in results and results["test2"].get("success"):
            try:
                results["test5"] = {"name": "Direct bcrypt check"}
                user = facade.get_user_by_email(email)
                import bcrypt
                pw_bytes = password.encode('utf-8')
                hash_bytes = user.password.encode('utf-8')
                result = bcrypt.checkpw(pw_bytes, hash_bytes)
                results["test5"]["success"] = True
                results["test5"]["password_verified"] = result
            except Exception as e:
                results["test5"]["success"] = False
                results["test5"]["error"] = str(e)
                
        # Test 6: SQLite direct check
        try:
            results["test6"] = {"name": "SQLite direct check"}
            import sqlite3
            conn = sqlite3.connect('../instance/development.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, password FROM users WHERE email=?", (email,))
            row = cursor.fetchone()
            
            if row:
                user_id, db_password = row
                results["test6"]["user_found"] = True
                results["test6"]["user_id"] = user_id
                
                import bcrypt
                pw_bytes = password.encode('utf-8')
                hash_bytes = db_password.encode('utf-8')
                result = bcrypt.checkpw(pw_bytes, hash_bytes)
                results["test6"]["password_verified"] = result
            else:
                results["test6"]["user_found"] = False
        except Exception as e:
            results["test6"]["success"] = False
            results["test6"]["error"] = str(e)
            
        return results

def verify_password(self, password):
    print(f"*** verify_password called with password: {password}")
    print(f"*** stored hash: {self.password}")
    try:
        # Convertir le mot de passe en bytes
        password_bytes = password.encode('utf-8') if isinstance(password, str) else password
        
        # Convertir le hash en bytes
        hash_bytes = self.password.encode('utf-8') if isinstance(self.password, str) else self.password
        
        # Vérification directe avec bcrypt
        import bcrypt
        return bcrypt.checkpw(password_bytes, hash_bytes)
        
    except Exception as e:
        print(f"Password verification error: {str(e)}")
        return False