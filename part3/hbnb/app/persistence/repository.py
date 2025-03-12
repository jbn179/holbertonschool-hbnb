from abc import ABC, abstractmethod
from app import db  # Assuming you have set up SQLAlchemy in your Flask app

class Repository(ABC):
    @abstractmethod
    def add(self, obj):
        pass

    @abstractmethod
    def get(self, obj_id):
        pass

    @abstractmethod
    def get_all(self):
        pass

    @abstractmethod
    def update(self, obj_id, data):
        pass

    @abstractmethod
    def delete(self, obj_id):
        pass

    @abstractmethod
    def get_by_attribute(self, attr_name, attr_value):
        pass


class InMemoryRepository(Repository):
    def __init__(self):
        self._storage = {}

    def add(self, obj):
        self._storage[obj.id] = obj

    def get(self, obj_id):
        return self._storage.get(obj_id)

    def get_all(self):
        return list(self._storage.values())

    def update(self, obj_id, data):
        obj = self.get(obj_id)
        if obj:
            obj.update(data)

    def delete(self, obj_id):
        if obj_id in self._storage:
            del self._storage[obj_id]
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        return next((obj for obj in self._storage.values() if getattr(obj, attr_name) == attr_value), None)

    def get_by_email(self, email):
        return self.get_by_attribute('email', email)


class SQLAlchemyRepository(Repository):
    def __init__(self, model):
        self.model = model

    def add(self, obj):
        """Add an object to the database"""
        db.session.add(obj)
        db.session.commit()
        return obj

    def get(self, obj_id):
        """Get an object by its ID"""
        return self.model.query.get(obj_id)

    def get_all(self):
        """Get all objects of this model"""
        return self.model.query.all()

    def update(self, obj_id, data):
        """Update an object with new data"""
        obj = self.get(obj_id)
        if obj:
            for key, value in data.items():
                setattr(obj, key, value)
            db.session.commit()
            return obj
        return None

    def delete(self, obj_id):
        """Delete an object by its ID"""
        obj = self.get(obj_id)
        if obj:
            db.session.delete(obj)
            db.session.commit()
            return True
        return False

    def get_by_attribute(self, attr_name, attr_value):
        """Find an object by a specific attribute"""
        return self.model.query.filter_by(**{attr_name: attr_value}).first()
    
    def get_by_email(self, email):
        """Find a user by email - convenience method"""
        return self.get_by_attribute('email', email)
