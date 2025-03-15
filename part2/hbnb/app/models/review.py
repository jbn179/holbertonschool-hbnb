from .base_model import BaseModel
from .user import User
from .place import Place

class Review(BaseModel):
    def __init__(self, text, rating, user, place):
        super().__init__()
        self.text = text
        self._rating = 0
        self.user = user
        self.place = place
        self.rating = rating
        self.validate()

    @property
    def rating(self):
        return self._rating

    @rating.setter
    def rating(self, value):
        if not isinstance(value, int) or not 1 <= value <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")
        self._rating = value

    def validate(self):
        """Validate review attributes"""
        if not self.text or not self.text.strip():
            raise ValueError("Text is required and cannot be empty")
        if len(self.text) > 1000:
            raise ValueError("Text must be 1000 characters or less")
        if not isinstance(self.user, User):
            raise ValueError("User must be a User instance")
        if not isinstance(self.place, Place):
            raise ValueError("Place must be a Place instance")
        if not isinstance(self.rating, int) or not 1 <= self.rating <= 5:
            raise ValueError("Rating must be an integer between 1 and 5")

    def to_dict(self):
        """Convert the review object to a dictionary"""
        review_dict = super().to_dict()
        review_dict.update({
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id,
            'place_id': self.place.id
        })
        return review_dict

    def update(self, data):
        """Update review attributes"""
        for key, value in data.items():
            setattr(self, key, value)
        self.validate()
