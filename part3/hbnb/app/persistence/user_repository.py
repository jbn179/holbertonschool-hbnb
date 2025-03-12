from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find a user by their email address"""
        return self.model.query.filter_by(email=email).first()
        
    def find_by_name(self, first_name=None, last_name=None):
        """Find users by first name, last name, or both"""
        query = self.model.query
        if first_name:
            query = query.filter(self.model.first_name.like(f"%{first_name}%"))
        if last_name:
            query = query.filter(self.model.last_name.like(f"%{last_name}%"))
        return query.all()
        
    def get_admins(self):
        """Get all admin users"""
        return self.model.query.filter_by(is_admin=True).all()
        
    def check_email_exists(self, email):
        """Check if an email is already registered"""
        return self.model.query.filter_by(email=email).count() > 0