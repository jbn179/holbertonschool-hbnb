from app import db
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity

class Place(BaseModel):
    """Place model representing a rental property"""
    __tablename__ = 'places'
    
    title = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(1024), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    
    # Foreign key reference to User
    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    
    # Establish relationship with User
    user = relationship("User", back_populates="places")
    
    # Establish one-to-many relationship with Review
    reviews = relationship("Review", back_populates="place", cascade="all, delete-orphan")
    
    # Establish many-to-many relationship with Amenity
    amenities = relationship("Amenity", secondary=place_amenity, back_populates="places")
    
    @validates('title')
    def validate_title(self, key, title):
        """Validate the title"""
        if not title or len(title.strip()) == 0:
            raise ValueError("Title cannot be empty")
        if len(title) > 128:
            raise ValueError("Title cannot exceed 128 characters")
        return title
        
    @validates('price')
    def validate_price(self, key, price):
        """Validate the price"""
        if price is None:
            raise ValueError("Price cannot be empty")
        if price < 0:
            raise ValueError("Price cannot be negative")
        return price
        
    @validates('latitude', 'longitude')
    def validate_coordinates(self, key, value):
        """Validate the latitude and longitude"""
        if value is None:
            raise ValueError(f"{key} cannot be empty")
        if not (-90 <= value <= 90) and key == 'latitude':
            raise ValueError("Latitude must be between -90 and 90 degrees")
        if not (-180 <= value <= 180) and key == 'longitude':
            raise ValueError("Longitude must be between -180 and 180 degrees")
        return value
