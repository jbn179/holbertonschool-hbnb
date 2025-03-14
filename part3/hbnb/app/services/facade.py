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
import uuid

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
    
    def create_amenity(self, data):
        """Create a new amenity"""
        # Validation explicite -> Explicit validation
        if 'name' not in data:
            raise ValueError("Missing required field: name")
        
        if not isinstance(data['name'], str):
            raise ValueError("Amenity name must be a string")
        
        if not data['name'].strip():
            raise ValueError("Amenity name cannot be empty")
        
        # Création de l'amenity -> Create the amenity
        new_amenity = Amenity(
            id=str(uuid.uuid4()),
            name=data['name'].strip()
        )
        
        # Persist to database en utilisant le repository -> Persist to database using the repository
        self.amenity_repo.add(new_amenity)
        
        return new_amenity

    def get_amenity(self, amenity_id):
        """Gets an amenity by ID"""
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        """Gets all amenities"""
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, data):
        """Updates an amenity"""
        # Validation du nom si présent -> Validate name if present
        if 'name' in data:
            if not isinstance(data['name'], str):
                raise ValueError("Amenity name must be a string")
            
            if not data['name'].strip():
                raise ValueError("Amenity name cannot be empty")
            
            data['name'] = data['name'].strip()
        
        # Mise à jour de l'aménité -> Update the amenity
        return self.amenity_repo.update(amenity_id, data)

    def find_amenity_by_name(self, name):
        """Finds an amenity by name"""
        return self.amenity_repo.find_by_name(name)
    
    # ========== PLACE METHODS ==========
    
    def create_place(self, place_data):
        """Creates a new place after validating owner and amenities"""
        try:
            # Cloner les données pour ne pas modifier l'original -> Clone data to avoid modifying the original
            place_data_copy = place_data.copy()
            
            # Extraire les amenities de place_data pour les traiter séparément -> Extract amenities from place_data to process separately
            amenities_ids = place_data_copy.pop('amenities', [])
            
            # Validate owner
            user_id = place_data_copy.get('user_id')
            if not user_id:
                raise ValueError("User ID is required")
                
            owner = self.get_user_by_id(user_id)
            if not owner:
                raise ValueError(f"User with ID {user_id} does not exist")
                
            # Generate ID if not provided
            if 'id' not in place_data_copy:
                place_data_copy['id'] = str(uuid.uuid4())
            
            # Set timestamps if not provided
            now = datetime.utcnow()
            if 'created_at' not in place_data_copy:
                place_data_copy['created_at'] = now
            if 'updated_at' not in place_data_copy:
                place_data_copy['updated_at'] = now
        
            # Create the place first without amenities
            place = Place(**place_data_copy)
            
            # Add amenities to the place if any
            if amenities_ids:
                for amenity_id in amenities_ids:
                    amenity = self.get_amenity(amenity_id)
                    if not amenity:
                        raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                    place.amenities.append(amenity)
            
            # Save the place with its amenities
            self.place_repo.add(place)
            return place
        except Exception as e:
            print(f"Error in create_place: {str(e)}")
            import traceback
            traceback.print_exc()
            raise  # Re-raise the exception after logging

    def get_place(self, place_id):
        """Gets a place by ID"""
        return self.place_repo.get(place_id)
        
    def get_all_places(self):
        """Gets all places"""
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        """Updates a place after validation"""
        place = self.get_place(place_id)
        if not place:
            return None
        
        # Extraire les amenities si présentes pour les traiter séparément
        amenities_ids = None
        if 'amenities' in place_data:
            amenities_ids = place_data.pop('amenities')
        
        # Validate owner if changed
        if 'user_id' in place_data:
            owner = self.get_user_by_id(place_data.get('user_id'))
            if not owner:
                raise ValueError(f"User with ID {place_data.get('user_id')} does not exist")
        
        # Update amenities if provided
        if amenities_ids is not None:
            # Clear existing amenities
            place.amenities = []
            
            # Add new amenities
            for amenity_id in amenities_ids:
                amenity = self.get_amenity(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} does not exist")
                place.amenities.append(amenity)
        
        # Update other fields
        for key, value in place_data.items():
            setattr(place, key, value)
        
        self.place_repo.update(place_id, {})  # Empty dict because we've already updated the place object
        return place

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
                amenity = self.get_amenity(amenity_id)
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

    def delete_place(self, place_id):
        """Delete a place"""
        # La vérification d'autorisation est déjà faite dans l'API
        return self.place_repo.delete(place_id)
        
    def find_places_by_price_range(self, min_price, max_price):
        """Finds places within a price range"""
        return self.place_repo.find_by_price_range(min_price, max_price)
    
    # ========== REVIEW METHODS ==========
    
    def create_review(self, review_data):
        """Creates a new review after validation"""
        try:
            # Clone the data to avoid modifying the original
            data = review_data.copy()
            
            # Validate user
            user_id = data.get('user_id')
            if not user_id:
                raise ValueError("User ID is required")
            
            user = self.get_user_by_id(user_id)
            if not user:
                raise ValueError(f"User with ID {user_id} does not exist")
            
            # Validate place
            place_id = data.get('place_id')
            if not place_id:
                raise ValueError("Place ID is required")
            
            place = self.get_place(place_id)
            if not place:
                raise ValueError(f"Place with ID {place_id} does not exist")
            
            # Generate ID if not provided
            if 'id' not in data:
                data['id'] = str(uuid.uuid4())
            
            # Set timestamps
            now = datetime.utcnow()
            data['created_at'] = now
            data['updated_at'] = now
            
            # Create review instance
            from app.models.review import Review
            new_review = Review(
                id=data['id'],
                user_id=data['user_id'],
                place_id=data['place_id'],
                text=data['text'],
                rating=float(data['rating']),
                created_at=data['created_at'],
                updated_at=data['updated_at']
            )
            
            # Add to database
            self.review_repo.add(new_review)
            return new_review
        except Exception as e:
            print(f"Error in create_review: {str(e)}")
            import traceback
            traceback.print_exc()
            raise  # Re-raise to let the endpoint handle it

    def get_review(self, review_id):
        """Gets a review by ID"""
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
