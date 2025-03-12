import uuid
from datetime import datetime
from app import db

class BaseModel:
    # Pour SQLAlchemy, ces attributs doivent être définis dans chaque modèle
    # Mais vous pouvez garder cette logique commune
    
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = self.created_at
    
    def save(self):
        """Update the updated_at timestamp whenever the object is modified"""
        self.updated_at = datetime.now()

    def update(self, data):
        """Update attributes of the model"""
        for key, value in data.items():
            if key not in ['id', 'created_at']:  # Ne pas modifier ces attributs
                setattr(self, key, value)
        self.updated_at = datetime.now()
