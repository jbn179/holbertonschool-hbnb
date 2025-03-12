from app.models.amenity import Amenity
from app.persistence.repository import SQLAlchemyRepository

class AmenityRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Amenity)
    
    def find_by_name(self, name):
        """Find amenity by name (exact match)"""
        return self.model.query.filter_by(name=name).first()
    
    def find_by_name_like(self, name_pattern):
        """Find amenities with names containing the pattern"""
        return self.model.query.filter(self.model.name.like(f"%{name_pattern}%")).all()
