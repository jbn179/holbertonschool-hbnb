import uuid
import sqlite3
import os

def seed_amenities():
    """Insert initial amenities into the database"""
    
    # Définir le chemin de la base de données SQLite
    db_path = os.path.join(os.path.dirname(__file__), 'instance', 'hbnb.db')
    
    # Vérifier si le répertoire existe, sinon le créer
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    
    # Créer la connexion à la base de données
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    
    try:
        # Vérifier si la table amenities existe, sinon la créer
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS amenities (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL UNIQUE,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
        ''')
        
        # Définir les équipements initiaux
        initial_amenities = [
            "Wi-Fi",
            "Piscine", 
            "Climatisation"
        ]
        
        # Insérer les équipements s'ils n'existent pas déjà
        for amenity_name in initial_amenities:
            cursor.execute("SELECT id FROM amenities WHERE name = ?", (amenity_name,))
            result = cursor.fetchone()
            
            if not result:
                amenity_id = str(uuid.uuid4())
                cursor.execute(
                    "INSERT INTO amenities (id, name) VALUES (?, ?)",
                    (amenity_id, amenity_name)
                )
                print(f"Added amenity: {amenity_name} with ID {amenity_id}")
        
        # Valider les changements
        conn.commit()
        print("Initial amenities seeded successfully")
    
    except Exception as e:
        conn.rollback()
        print(f"Error seeding amenities: {str(e)}")
    
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    seed_amenities()