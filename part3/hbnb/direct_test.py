import sqlite3
import bcrypt

# Connexion à la base de données
try:
    conn = sqlite3.connect('../instance/development.db')
    cursor = conn.cursor()
    print("Connexion à la base de données réussie!")
    
    # Récupération du hash depuis la base de données
    cursor.execute("SELECT password FROM users WHERE email=?", ('admin@hbnb.io',))
    result = cursor.fetchone()
    
    if not result:
        print("Utilisateur admin non trouvé dans la base de données!")
    else:
        db_hash = result[0]
        print(f"Hash trouvé dans la DB: {db_hash}")
        
        # Test du mot de passe
        password = 'admin1234'
        print(f"Test avec mot de passe: {password}")
        
        # Vérification avec bcrypt
        try:
            # Convertir le mot de passe en bytes
            password_bytes = password.encode('utf-8')
            # Convertir le hash en bytes si nécessaire
            hash_bytes = db_hash.encode('utf-8') if isinstance(db_hash, str) else db_hash
            
            # Vérification
            result = bcrypt.checkpw(password_bytes, hash_bytes)
            print(f"Résultat de la vérification bcrypt: {result}")
            
        except Exception as e:
            print(f"Erreur lors de la vérification bcrypt: {str(e)}")
            
except sqlite3.Error as e:
    print(f"Erreur SQLite: {str(e)}")
except Exception as e:
    print(f"Erreur générale: {str(e)}")
finally:
    if 'conn' in locals() and conn:
        conn.close()
        print("Connexion à la base de données fermée.")