from .base_model import BaseModel
from .user import User

class Place(BaseModel):
    def __init__(self, title, description, price, latitude, longitude, owner):
        super().__init__()
        self.title = title
        self.description = description
        self._price = 0
        self._latitude = 0
        self._longitude = 0
        self.owner = owner
        self.amenities = []
        self.reviews = []
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.validate()

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if not isinstance(value, (int, float)) or value <= 0:
            raise ValueError("Price must be a positive number")
        self._price = float(value)

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not isinstance(value, (int, float)) or not -90 <= value <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        self._latitude = float(value)

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not isinstance(value, (int, float)) or not -180 <= value <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        self._longitude = float(value)

    def validate(self):
        """Validate place attributes"""
        if not self.title or not self.title.strip():
            raise ValueError("Title is required and cannot be empty")
        if len(self.title) > 100:
            raise ValueError("Title must be 100 characters or less")
        if not isinstance(self.owner, User):
            raise ValueError("Owner must be a User instance")
        if not isinstance(self.price, (int, float)) or self.price <= 0:
            raise ValueError("Price must be a positive number")
        if not isinstance(self.latitude, (int, float)) or not -90 <= self.latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90")
        if not isinstance(self.longitude, (int, float)) or not -180 <= self.longitude <= 180:
            raise ValueError("Longitude must be between -180 and 180")
        if not isinstance(self.description, str):
            raise ValueError("Description must be a string")

    def add_amenity(self, amenity_id):
        """Add an amenity ID to the place"""
        if amenity_id not in self.amenities:
            self.amenities.append(amenity_id)

    def add_review(self, review):
        """Add a review to the place"""
        if review not in self.reviews:
            self.reviews.append(review)

    def to_dict(self):
        """Convert the place object to a dictionary"""
        place_dict = super().to_dict()
        place_dict.update({
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id,
            'amenities': self.amenities,
            'reviews': [review.id for review in self.reviews]
        })
        return place_dict

    def update(self, data):
        """Update place attributes"""
        for key, value in data.items():
            setattr(self, key, value)
        self.validate()
