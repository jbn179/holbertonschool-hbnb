from app import create_app, db
import os
import sqlalchemy as sa

def recreate_database():
    app = create_app()
    with app.app_context():
        # Trouver le chemin de la base de données
        db_uri = app.config.get('SQLALCHEMY_DATABASE_URI')
        if db_uri.startswith('sqlite:///'):
            db_path = db_uri.replace('sqlite:///', '')
            # Si c'est un chemin relatif, convertir en absolu
            if not os.path.isabs(db_path):
                db_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), db_path)
            
            print(f"DB Path: {db_path}")
            
            # Supprimer le fichier si existant
            if os.path.exists(db_path):
                print(f"Suppression de la base de données existante: {db_path}")
                os.remove(db_path)
        
        # Supprimer toutes les tables et les recréer
        print("Suppression de toutes les tables...")
        db.drop_all()
        print("Création de toutes les tables...")
        db.create_all()
        print("Base de données recréée avec succès!")

if __name__ == "__main__":
    recreate_database()