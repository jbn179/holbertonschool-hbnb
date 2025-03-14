import sqlite3
import bcrypt

# Connexion directe à la base de données
conn = sqlite3.connect('instance/development.db')
cursor = conn.cursor()

# Email et mot de passe à tester
email = "testuser@example.com"
password = "password123"

print(f"Testing authentication for {email} with password {password}")

# Récupérer l'utilisateur depuis SQLite
cursor.execute("SELECT id, password, first_name, last_name, is_admin FROM users WHERE email=?", (email,))
user = cursor.fetchone()

if not user:
    print("User not found in database!")
else:
    user_id, pw_hash, first_name, last_name, is_admin = user
    print(f"User found: {first_name} {last_name}")
    print(f"User ID: {user_id}")
    print(f"Admin: {bool(is_admin)}")
    print(f"Password hash: {pw_hash}")
    
    # Test direct avec bcrypt
    try:
        pw_bytes = password.encode('utf-8')
        hash_bytes = pw_hash.encode('utf-8')
        result = bcrypt.checkpw(pw_bytes, hash_bytes)
        print(f"Direct bcrypt verification result: {result}")
        
        # Simuler ce que User.verify_password pourrait faire différemment
        print("\nTesting various verification approaches:")
        
        # Test 1: Vérification standard
        print(f"1. Standard verification: {bcrypt.checkpw(pw_bytes, hash_bytes)}")
        
        # Test 2: Différentes encodages
        print(f"2. With UTF-8 encoding: {bcrypt.checkpw(password.encode('utf-8'), pw_hash.encode('utf-8'))}")
        
        # Test 3: Sans conversion en bytes (devrait échouer)
        try:
            result3 = bcrypt.checkpw(password, pw_hash)
            print(f"3. Without bytes conversion: {result3}")
        except Exception as e:
            print(f"3. Without bytes conversion: Error - {str(e)}")
            
    except Exception as e:
        print(f"Error during bcrypt verification: {str(e)}")

conn.close()