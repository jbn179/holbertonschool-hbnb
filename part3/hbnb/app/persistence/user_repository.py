from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        """Find a user by their email address"""
        print(f"Repository: looking for user with email '{email}'")
        
        # Essayer avec la méthode standard
        user = self.model.query.filter_by(email=email).first()
        
        if user:
            print(f"Repository: found user with ID {user.id}")
            return user
            
        # Solution de secours : utiliser directement SQLite
        import sqlite3
        try:
            conn = sqlite3.connect('../instance/development.db')
            cursor = conn.cursor()
            cursor.execute("SELECT id, first_name, last_name, email, password, is_admin FROM users WHERE email=?", (email,))
            row = cursor.fetchone()
            
            if row:
                print(f"Repository: found user in direct SQL with ID {row[0]}")
                # Créer un objet User avec les données de la BDD
                from app.models.user import User
                user = User()
                user.id = row[0]
                user.first_name = row[1]
                user.last_name = row[2]
                user.email = row[3]
                user.password = row[4]
                user.is_admin = bool(row[5])
                return user
        except Exception as e:
            print(f"Repository error: {str(e)}")
        finally:
            if 'conn' in locals():
                conn.close()
                
        print("Repository: no user found")
        return None
        
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