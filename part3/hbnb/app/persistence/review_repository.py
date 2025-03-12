from app.models.review import Review
from app.persistence.repository import SQLAlchemyRepository

class ReviewRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Review)
    
    def find_by_place(self, place_id):
        """Find all reviews for a specific place"""
        return self.model.query.filter_by(place_id=place_id).all()
    
    def find_by_user(self, user_id):
        """Find all reviews by a specific user"""
        return self.model.query.filter_by(user_id=user_id).all()
    
    def find_by_rating(self, min_rating, max_rating=5):
        """Find reviews within a rating range"""
        return self.model.query.filter(
            self.model.rating >= min_rating,
            self.model.rating <= max_rating
        ).all()
    
    def get_average_rating_for_place(self, place_id):
        """Get the average rating for a place"""
        from sqlalchemy import func
        result = db.session.query(func.avg(self.model.rating))\
                           .filter(self.model.place_id == place_id)\
                           .scalar()
        return result if result else 0
