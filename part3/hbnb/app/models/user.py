from app import db, bcrypt
from app.models.basemodel import BaseModel
from sqlalchemy.orm import validates, relationship
import re

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)
    
    # Establish one-to-many relationship with Place
    places = relationship("Place", back_populates="user", cascade="all, delete-orphan")
    
    # Establish one-to-many relationship with Review
    reviews = relationship("Review", back_populates="user", cascade="all, delete-orphan")

    def hash_password(self, password):
        """Hash the password before storing it."""
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verify the hashed password."""
        return bcrypt.check_password_hash(self.password, password)
        
    @validates('first_name')
    def validate_first_name(self, key, first_name):
        """Validates the first name"""
        if not first_name or len(first_name.strip()) == 0:
            raise ValueError("First name cannot be empty")
        if len(first_name) > 50:
            raise ValueError("First name cannot exceed 50 characters")
        return first_name
        
    @validates('last_name')
    def validate_last_name(self, key, last_name):
        """Validates the last name"""
        if not last_name or len(last_name.strip()) == 0:
            raise ValueError("Last name cannot be empty")
        if len(last_name) > 50:
            raise ValueError("Last name cannot exceed 50 characters")
        return last_name
        
    @validates('email')
    def validate_email(self, key, email):
        """Validates the email address"""
        if not email or len(email.strip()) == 0:
            raise ValueError("Email cannot be empty")
        # Simple regex for email validation
        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")
        return email
        
    @validates('password')
    def validate_password(self, key, password):
        """Validates the password before hashing"""
        if not password or len(password) < 8:
            raise ValueError("Password must be at least 8 characters long")
        # You could add other complexity rules here
        return password
