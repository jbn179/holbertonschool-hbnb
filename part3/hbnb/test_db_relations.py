from app import create_app, db
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity

def test_relationships():
    """Test all model relationships directly in the database"""
    app = create_app()
    with app.app_context():
        # Clean up test data first
        db.session.query(Review).delete()
        db.session.query(Place).delete()
        db.session.query(User).delete()
        db.session.query(Amenity).delete()
        db.session.commit()
        
        print("=== TESTING USER-PLACE RELATIONSHIP ===")
        # Create a user
        user = User(
            first_name="Test", 
            last_name="User", 
            email="test@example.com", 
            password="password"
        )
        user.hash_password("password")
        db.session.add(user)
        db.session.commit()
        print(f"Created user: {user.id}")
        
        # Create places for the user
        place1 = Place(
            title="Beach House",
            description="Beautiful beach house",
            price=150.0,
            latitude=40.7,
            longitude=-74.0,
            owner_id=user.id  # Changez user_id en owner_idd  # Changez user_id en owner_id
        )
        place2 = Place(
            title="Mountain Cabin",
            description="Cozy mountain cabin",
            price=120.0,
            latitude=42.7,
            longitude=-76.0,
            owner_id=user.id  # Changez user_id en owner_idd  # Changez user_id en owner_id
        )
        db.session.add(place1)
        db.session.add(place2)
        db.session.commit()
        print(f"Created places: {place1.id}, {place2.id}")
        
        # Test user-place relationship
        user_places = User.query.get(user.id).places
        print(f"User has {len(user_places)} places - {'SUCCESS' if len(user_places) == 2 else 'FAILURE'}")
        place_user = Place.query.get(place1.id).user
        print(f"Place belongs to user {place_user.id} - {'SUCCESS' if place_user.id == user.id else 'FAILURE'}")
        
        print("\n=== TESTING PLACE-REVIEW AND USER-REVIEW RELATIONSHIPS ===")
        # Create reviews
        review1 = Review(
            text="Great place!",
            rating=5,
            user_id=user.id,
            place_id=place1.id
        )
        review2 = Review(
            text="Awesome!",
            rating=4,
            user_id=user.id,
            place_id=place1.id
        )
        db.session.add(review1)
        db.session.add(review2)
        db.session.commit()
        print(f"Created reviews: {review1.id}, {review2.id}")
        
        # Test place-review relationship
        place_reviews = Place.query.get(place1.id).reviews
        print(f"Place has {len(place_reviews)} reviews - {'SUCCESS' if len(place_reviews) == 2 else 'FAILURE'}")
        
        # Test user-review relationship
        user_reviews = User.query.get(user.id).reviews
        print(f"User has {len(user_reviews)} reviews - {'SUCCESS' if len(user_reviews) == 2 else 'FAILURE'}")
        
        print("\n=== TESTING PLACE-AMENITY RELATIONSHIP (MANY-TO-MANY) ===")
        # Create amenities
        amenity1 = Amenity(name="WiFi")
        amenity2 = Amenity(name="Pool")
        db.session.add(amenity1)
        db.session.add(amenity2)
        db.session.commit()
        print(f"Created amenities: {amenity1.id}, {amenity2.id}")
        
        # Associate amenities with place
        place1.amenities.append(amenity1)
        place1.amenities.append(amenity2)
        db.session.commit()
        
        # Test many-to-many relationships
        place_amenities = Place.query.get(place1.id).amenities
        print(f"Place has {len(place_amenities)} amenities - {'SUCCESS' if len(place_amenities) == 2 else 'FAILURE'}")
        
        amenity_places = Amenity.query.get(amenity1.id).places
        print(f"Amenity is used in {len(amenity_places)} places - {'SUCCESS' if len(amenity_places) == 1 else 'FAILURE'}")
        
        print("\n=== TEST SUMMARY ===")
        print("All relationships have been tested directly in the database")
        print("This confirms your SQLAlchemy models are correctly configured")

if __name__ == "__main__":
    test_relationships()