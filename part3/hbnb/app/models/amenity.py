from app import db
import uuid
from datetime import datetime
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity

class Amenity(db.Model):
    """Amenity model representing facilities available in places"""
    __tablename__ = 'amenities'
    
    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    name = db.Column(db.String(128), nullable=False, unique=True)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    # La relation many-to-many avec Place est déjà définie via backref dans le modèle Place

    @validates('name')
    def validate_name(self, key, name):
        """Validates the amenity name"""
        # Vérifiez d'abord que name est une chaîne
        if not isinstance(name, str):
            raise ValueError("Amenity name must be a string")
            
        # Maintenant, vous pouvez appliquer strip() en toute sécurité
        if not name or len(name.strip()) == 0:
            raise ValueError("Amenity name cannot be empty")
        return name
