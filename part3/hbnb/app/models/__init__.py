# Exportez vos modèles pour qu'ils soient accessibles via app.models
from app.models.user import User
from app.models.place import Place
from app.models.review import Review
from app.models.amenity import Amenity
from app.models.base_model import BaseModel

# Exportez tous les modèles pour qu'ils soient disponibles lors de l'import de app.models
__all__ = ['User', 'Place', 'Review', 'Amenity', 'BaseModel']