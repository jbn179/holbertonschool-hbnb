from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)
        
    def find_by_price_range(self, min_price, max_price):
        """Find places within a specific price range"""
        return self.model.query.filter(
            self.model.price >= min_price,
            self.model.price <= max_price
        ).all()
        
    def find_by_location(self, lat, lng, radius=10):
        """Find places within a specific radius (in km) of a location
        Uses a simple approximation for demonstration purposes"""
        return self.model.query.filter(
            self.model.latitude.between(lat - radius/111, lat + radius/111),
            self.model.longitude.between(lng - radius/111, lng + radius/111)
        ).all()