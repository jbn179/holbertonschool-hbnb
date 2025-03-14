import os
import sys
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))

try:
    # Créer un lien symbolique pour résoudre l'importation
    import subprocess
    subprocess.call(['ln', '-sf', 'hbnb/app', 'app'])
    
    # Importer les modules
    from hbnb.app import create_app
    from hbnb.app.models.user import User
    import bcrypt
    
    app = create_app()
    
    with app.app_context():
        # Email et mot de passe de test
        email = "testuser@example.com"
        password = "password123"
        
        print(f"Testing authentication for {email}")
        
        # Récupérer l'utilisateur
        user = User.query.filter_by(email=email).first()
        
        if not user:
            print("User not found!")
        else:
            print(f"User found: {user.email}")
            print(f"User ID: {user.id}")
            print(f"Admin: {user.is_admin}")
            print(f"Password hash: {user.password}")
            
            # Test direct avec bcrypt
            pw_bytes = password.encode('utf-8')
            hash_bytes = user.password.encode('utf-8')
            result = bcrypt.checkpw(pw_bytes, hash_bytes)
            
            print(f"Direct bcrypt verification: {result}")
            
            # Test avec la méthode verify_password
            result2 = user.verify_password(password)
            print(f"User.verify_password result: {result2}")
            
except Exception as e:
    print(f"Error: {str(e)}")