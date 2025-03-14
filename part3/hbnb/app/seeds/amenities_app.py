import uuid
from app import create_app, db
from app.models.amenity import Amenity

def seed_amenities():
    """Insert initial amenities into the application database"""
    app = create_app()
    with app.app_context():
        # Define initial amenities
        initial_amenities = [
            "Wi-Fi",
            "Piscine", 
            "Climatisation"
        ]
        
        # Insert amenities if they don't exist
        for amenity_name in initial_amenities:
            existing = Amenity.query.filter_by(name=amenity_name).first()
            
            if not existing:
                new_amenity = Amenity(
                    id=str(uuid.uuid4()),
                    name=amenity_name
                )
                db.session.add(new_amenity)
                print(f"Added amenity: {amenity_name}")
        
        # Commit changes
        db.session.commit()
        print("Initial amenities seeded successfully")

if __name__ == "__main__":
    seed_amenities()