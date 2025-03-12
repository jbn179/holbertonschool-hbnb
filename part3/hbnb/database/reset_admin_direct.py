import sqlite3
import bcrypt
import os

# Chemin vers la base de données
db_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'instance', 'development.db'))
print(f"Connexion à la base de données: {db_path}")

# Connexion à la base de données
conn = sqlite3.connect(db_path)
cursor = conn.cursor()

# Afficher le hash actuel
cursor.execute("SELECT password FROM users WHERE email = 'admin@hbnb.io'")
result = cursor.fetchone()

if not result:
    print("Administrateur non trouvé!")
    conn.close()
    exit(1)

current_hash = result[0]
print(f"Hash actuel: {current_hash}")

# Générer un nouveau hash pour 'admin1234'
password = 'admin1234'
salt = bcrypt.gensalt()
new_hash = bcrypt.hashpw(password.encode('utf-8'), salt).decode('utf-8')
print(f"Nouveau hash: {new_hash}")

# Mettre à jour le mot de passe
cursor.execute("UPDATE users SET password = ? WHERE email = 'admin@hbnb.io'", (new_hash,))
conn.commit()
print("Mot de passe mis à jour avec succès!")

# Vérifier la mise à jour
cursor.execute("SELECT password FROM users WHERE email = 'admin@hbnb.io'")
updated_hash = cursor.fetchone()[0]
print(f"Hash mis à jour: {updated_hash}")

# Fermer la connexion
conn.close()