from app.persistence.repository import SQLAlchemyRepository
from app.models.review import Review
from app import db

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    
    def get_reviews_by_place(self, place_id):
        """Get all reviews for a specific place"""
        return Review.query.filter_by(place_id=place_id).all()
    
    def get_reviews_by_user(self, user_id):
        """Get all reviews by a specific user"""
        return Review.query.filter_by(user_id=user_id).all()
    
    def get_all(self):
        """Get all reviews"""
        return Review.query.all()
