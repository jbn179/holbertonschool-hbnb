from app import db
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity

class Amenity(BaseModel):
    """Amenity model representing facilities available in places"""
    __tablename__ = 'amenities'
    
    name = db.Column(db.String(50), nullable=False, unique=True)
    
    # Establish many-to-many relationship with Place
    places = relationship("Place", secondary=place_amenity, back_populates="amenities")

    @validates('name')
    def validate_name(self, key, name):
        """Validate amenity name"""
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        if len(name) > 50:
            raise ValueError("Amenity name cannot exceed 50 characters")
        return name
