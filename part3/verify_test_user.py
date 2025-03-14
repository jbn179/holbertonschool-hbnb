import sqlite3
import bcrypt

try:
    # Connexion à la base de données
    conn = sqlite3.connect('instance/development.db')
    cursor = conn.cursor()
    
    # Récupérer le hash de l'utilisateur test
    cursor.execute("SELECT password FROM users WHERE email = ?", ('testuser@example.com',))
    result = cursor.fetchone()
    
    if result:
        db_hash = result[0]
        print(f"Hash trouvé dans la DB: {db_hash}")
        
        # Test du mot de passe
        password = 'password123'
        print(f"Test avec mot de passe: {password}")
        
        # Vérification avec bcrypt
        try:
            password_bytes = password.encode('utf-8')
            hash_bytes = db_hash.encode('utf-8')
            
            result = bcrypt.checkpw(password_bytes, hash_bytes)
            print(f"Résultat de la vérification bcrypt: {result}")
        except Exception as e:
            print(f"Erreur lors de la vérification bcrypt: {str(e)}")
    else:
        print("Utilisateur test non trouvé dans la base de données!")
    
    # Fermer la connexion
    conn.close()
    
except Exception as e:
    print(f"Erreur: {str(e)}")