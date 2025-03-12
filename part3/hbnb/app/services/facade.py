from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository
from app.persistence.place_repository import PlaceRepository
from app.persistence.amenity_repository import AmenityRepository
from app.persistence.review_repository import ReviewRepository
from datetime import datetime

class HBnBFacade:
    def __init__(self):
        # Repositories
        self.user_repo = UserRepository()
        self.place_repo = PlaceRepository()
        self.amenity_repo = AmenityRepository()
        self.review_repo = ReviewRepository()

    # ========== USER METHODS ==========
    
    def create_user(self, user_data):
        """Creates a new user"""
        user = User(**user_data)
        if 'password' in user_data:
            user.hash_password(user_data['password'])
        self.user_repo.add(user)
        return user

    def get_user_by_id(self, user_id):
        """Gets a user by ID"""
        return self.user_repo.get(user_id)
        
    def get_user_by_email(self, email):
        """Gets a user by email"""
        return self.user_repo.get_user_by_email(email)

    def get_all_users(self):
        """Gets all users"""
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        """Updates a user"""
        user = self.get_user_by_id(user_id)
        if not user:
            return None
        self.user_repo.update(user_id, user_data)
        return self.get_user_by_id(user_id)

    def delete_user(self, user_id, current_user_id):
        """Only administrators can delete users"""
        current_user = self.user_repo.get(current_user_id)
        # An admin cannot delete themselves
        if current_user and current_user.is_admin and user_id != current_user_id:
            return self.user_repo.delete(user_id)
        return False
    
    # ========== AMENITY METHODS ==========
    
    def create_amenity(self, name):
        """Creates a new amenity"""
        amenity = Amenity(name=name)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity_by_id(self, amenity_id):
        """Gets an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Gets all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Updates an amenity"""
        return self.amenity_repo.update(amenity_id, data)

    def find_amenity_by_name(self, name):
        """Finds an amenity by name"""
        return self.amenity_repo.find_by_name(name)
    
    def delete_amenity(self, amenity_id, current_user_id):
        """Only administrators can delete amenities"""
        current_user = self.user_repo.get(current_user_id)
        if current_user and current_user.is_admin:
            return self.amenity_repo.delete(amenity_id)
        return False

    # ========== PLACE METHODS ==========
    
    def create_place(self, place_data):
        """Creates a new place after validating owner and amenities"""
        # Validate owner
        owner_id = place_data.get('owner_id')
        owner = self.get_user_by_id(owner_id)
        if not owner:
            raise ValueError(f"Owner with ID {owner_id} does not exist")

        # Validate amenities if provided
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity_by_id(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities
    
        # Create and save the place
        place = Place(**place_data)
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        """Gets a place by ID"""
        return self.place_repo.get(place_id)
        
    def get_place_by_id(self, place_id):
        """Alias for get_place"""
        return self.place_repo.get(place_id)

    def get_all_places(self):
        """Gets all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates a place after validation"""
        place = self.get_place(place_id)
        if not place:
            return None
    
        # Validate owner if changed
        if 'owner_id' in place_data:
            owner = self.get_user_by_id(place_data.get('owner_id'))
            if not owner:
                raise ValueError(f"Owner with ID {place_data.get('owner_id')} does not exist")
    
        # Validate amenities if changed
        if 'amenities' in place_data and place_data['amenities']:
            valid_amenities = []
            for amenity_id in place_data['amenities']:
                amenity = self.get_amenity_by_id(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                valid_amenities.append(amenity_id)
            place_data['amenities'] = valid_amenities
    
        # Update the place
        self.place_repo.update(place_id, place_data)
        return self.get_place(place_id)

    def get_place_with_details(self, place_id):
        """Gets a place with details about owner, amenities, and reviews"""
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Owner details
        owner = self.get_user_by_id(place.owner_id)
        owner_details = None
        if owner:
            owner_details = {
                'id': owner.id,
                'first_name': owner.first_name,
                'last_name': owner.last_name,
                'email': owner.email
            }
        
        # Amenity details
        amenity_details = []
        if hasattr(place, 'amenities') and place.amenities:
            for amenity_id in place.amenities:
                amenity = self.get_amenity_by_id(amenity_id)
                if amenity:
                    amenity_details.append({
                        'id': amenity.id,
                        'name': amenity.name
                    })
        
        # Review details
        review_details = []
        reviews = self.get_reviews_by_place(place_id)
        if reviews:
            for review in reviews:
                review_details.append({
                    'id': review.id,
                    'text': review.text,
                    'rating': review.rating,
                    'user_id': review.user_id
                })
        
        # Detailed response
        return {
            'id': place.id,
            'title': place.title,
            'description': place.description,
            'price': place.price,
            'latitude': place.latitude,
            'longitude': place.longitude,
            'owner': owner_details,
            'amenities': amenity_details,
            'reviews': review_details,
            'created_at': place.created_at if isinstance(place.created_at, str) else place.created_at.isoformat() if isinstance(place.created_at, datetime) else str(place.created_at),
            'updated_at': place.updated_at if isinstance(place.updated_at, str) else place.updated_at.isoformat() if isinstance(place.updated_at, datetime) else str(place.updated_at)
        }

    def delete_place(self, place_id, current_user_id):
        """Only administrators can delete places"""
        current_user = self.user_repo.get(current_user_id)
        if current_user and current_user.is_admin:
            return self.place_repo.delete(place_id)
        return False
        
    def find_places_by_price_range(self, min_price, max_price):
        """Finds places within a price range"""
        return self.place_repo.find_by_price_range(min_price, max_price)
    
    # ========== REVIEW METHODS ==========
    
    def create_review(self, review_data):
        """Creates a new review after validation"""
        # Validate user
        user = self.get_user_by_id(review_data.get('user_id'))
        if not user:
            raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place
        place = self.get_place(review_data.get('place_id'))
        if not place:
            raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Create and save the review
        review = Review(**review_data)
        self.review_repo.add(review)
        return review

    def get_review(self, review_id):
        """Gets a review by ID"""
        return self.review_repo.get(review_id)
        
    def get_review_by_id(self, review_id):
        """Alias for get_review"""
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        """Gets all reviews"""
        return self.review_repo.get_all()

    def update_review(self, review_id, review_data):
        """Updates a review after validation"""
        review = self.get_review(review_id)
        if not review:
            return None
        
        # Validate user if changed
        if 'user_id' in review_data:
            user = self.get_user_by_id(review_data.get('user_id'))
            if not user:
                raise ValueError(f"User with ID {review_data.get('user_id')} does not exist")
        
        # Validate place if changed
        if 'place_id' in review_data:
            place = self.get_place(review_data.get('place_id'))
            if not place:
                raise ValueError(f"Place with ID {review_data.get('place_id')} does not exist")
        
        # Update the review
        self.review_repo.update(review_id, review_data)
        return self.get_review(review_id)

    def get_reviews_by_place(self, place_id):
        """Gets all reviews for a specific place"""
        return self.review_repo.find_by_place(place_id)

    def get_average_rating_for_place(self, place_id):
        """Gets the average rating for a place"""
        return self.review_repo.get_average_rating_for_place(place_id)

    def delete_review(self, review_id, current_user_id):
        """Users can delete their own reviews, admins can delete any review"""
        review = self.review_repo.get(review_id)
        if not review:
            return False
        
        current_user = self.user_repo.get(current_user_id)
        
        # Admin can delete any review
        if current_user and current_user.is_admin:
            return self.review_repo.delete(review_id)
        
        # Users can only delete their own reviews
        if review.user_id == current_user_id:
            return self.review_repo.delete(review_id)
        
        return False

# Single instance of the facade
facade = HBnBFacade()
