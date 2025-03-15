from app.persistence.repository import InMemoryRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()
        self.amenity_repo = InMemoryRepository()

    # User-related methods
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, user_data):
        user = self.get_user(user_id)
        if user:
            user.update(user_data)
            self.user_repo.update(user)
            return user
        return None

    # Amenity-related methods
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if amenity:
            amenity.update(amenity_data)
            self.amenity_repo.update(amenity)
            return amenity
        return None

    # Place-related methods
    def create_place(self, place_data):
        owner = self.get_user(place_data['owner_id'])
        if not owner:
            raise ValueError("Owner not found")
        
        amenities = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.get_amenity(amenity_id)
            if amenity:
                amenities.append(amenity.id)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )
        place.amenities = amenities
        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        place = self.place_repo.get(place_id)
        if place:
            place.owner = self.get_user(place.owner.id)  # Ensure we have the full owner object
            place.amenities = [self.get_amenity(amenity_id) for amenity_id in place.amenities]  # Get full amenity objects
        return place

    def get_all_places(self):
        places = self.place_repo.get_all()
        for place in places:
            place.owner = self.get_user(place.owner.id)  # Ensure we have the full owner object
        return places

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if place:
            if 'owner_id' in place_data:
                owner = self.get_user(place_data['owner_id'])
                if not owner:
                    raise ValueError("Owner not found")
                place.owner = owner
            
            if 'amenities' in place_data:
                amenities = []
                for amenity_id in place_data['amenities']:
                    amenity = self.get_amenity(amenity_id)
                    if amenity:
                        amenities.append(amenity.id)
                place.amenities = amenities

            place.update(place_data)
            self.place_repo.update(place)
            return place
        return None

    # Review-related methods
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])

    # Review-related methods
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        place = self.get_place(review_data['place_id'])
        if not user or not place:
            raise ValueError("User or Place not found")
        
        review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user=user,
            place=place
        )
        self.review_repo.add(review)
        place.add_review(review)
        self.place_repo.update(place)
        return review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()

    def get_reviews_by_place(self, place_id):
        place = self.get_place(place_id)
        if not place:
            return None
        return place.reviews

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if review:
            review.update(review_data)
            self.review_repo.update(review)
            return review
        return None

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if review:
            place = self.get_place(review.place.id)
            place.reviews.remove(review)
            self.place_repo.update(place)
            self.review_repo.delete(review_id)
            return True
        return False

facade = HBnBFacade()
