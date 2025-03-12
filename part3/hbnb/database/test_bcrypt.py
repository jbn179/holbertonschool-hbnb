from flask_bcrypt import Bcrypt
bcrypt = Bcrypt()

# Hash actuel dans la base de données
stored_hash = '$2b$12$0elcbXPP0A7fm7PvaTTWp.IXECX9WCDHwgfVNB5WVrpwsz4AmkYjC'

# Test avec le mot de passe attendu
result = bcrypt.check_password_hash(stored_hash, 'admin1234')
print(f"Le mot de passe 'admin1234' est {'valide' if result else 'invalide'} pour ce hash")