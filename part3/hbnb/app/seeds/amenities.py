import uuid
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from app.models.amenity import Amenity

def seed_amenities():
    """
    Insert initial amenities into the database
    """
    # Create database connection
    # Replace with your actual database URL
    engine = create_engine('sqlite:///hbnb.db')  
    Session = sessionmaker(bind=engine)
    session = Session()
    
    # Define the initial amenities
    initial_amenities = [
        "Wi-Fi",
        "Piscine",
        "Climatisation"
    ]
    
    # Insert amenities if they don't exist
    for amenity_name in initial_amenities:
        existing = session.query(Amenity).filter_by(name=amenity_name).first()
        
        if not existing:
            new_amenity = Amenity(
                id=str(uuid.uuid4()),
                name=amenity_name
            )
            session.add(new_amenity)
            print(f"Added amenity: {amenity_name}")
    
    # Commit changes
    session.commit()
    session.close()
    print("Initial amenities seeded successfully")

if __name__ == "__main__":
    seed_amenities()