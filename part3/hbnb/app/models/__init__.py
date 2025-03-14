from app import db
# Importe d'abord les associations pour qu'elles soient disponibles pour les autres modèles
from app.models.associations import place_amenity  # Cette ligne est importante
# Ensuite importe les modèles qui utilisent ces associations
from app.models.user import User
from app.models.place import Place
from app.models.amenity import Amenity
from app.models.review import Review
from app.models.base_model import BaseModel

# Exportez tous les modèles pour qu'ils soient disponibles lors de l'import de app.models
__all__ = ['User', 'Place', 'Review', 'Amenity', 'BaseModel']