from app import db
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates, relationship

class Review(BaseModel):
    """Review model for place ratings and comments"""
    __tablename__ = 'reviews'
    
    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)
    
    # Foreign key to User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Relationship with User
    user = relationship("User", back_populates="reviews")
    
    # Foreign key to Place 
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)
    
    # Relationship with Place
    place = relationship("Place", back_populates="reviews")
    
    @validates('text')
    def validate_text(self, key, text):
        """Validate review text"""
        if not text or len(text.strip()) == 0:
            raise ValueError("Review text cannot be empty")
        if len(text) > 1024:
            raise ValueError("Review text cannot exceed 1024 characters")
        return text
    
    @validates('rating')
    def validate_rating(self, key, rating):
        """Validate review rating"""
        if rating is None:
            raise ValueError("Rating cannot be empty")
        
        # Essayer de convertir en int si ce n'est pas déjà un int
        try:
            rating_int = int(rating)
        except (ValueError, TypeError):
            raise ValueError("Rating must be convertible to an integer")
        
        if rating_int < 1 or rating_int > 5:
            raise ValueError("Rating must be between 1 and 5")
        return rating_int  # Retourner la version int
