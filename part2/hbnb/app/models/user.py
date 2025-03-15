from .base_model import BaseModel

class User(BaseModel):
    def __init__(self, first_name, last_name, email, is_admin=False):
        super().__init__()
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin
        self.validate()

    def validate(self):
        """Validate user attributes"""
        if not self.first_name or not self.first_name.strip():
            raise ValueError("First name is required and cannot be empty")
        if len(self.first_name) > 50:
            raise ValueError("First name must be 50 characters or less")
        if not self.last_name or not self.last_name.strip():
            raise ValueError("Last name is required and cannot be empty")
        if len(self.last_name) > 50:
            raise ValueError("Last name must be 50 characters or less")
        if not self.email or not self.email.strip():
            raise ValueError("Email is required and cannot be empty")
        if '@' not in self.email or '.' not in self.email:
            raise ValueError("Invalid email format")

    def to_dict(self):
        """Convert the user object to a dictionary"""
        user_dict = super().to_dict()
        user_dict.update({
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
            'is_admin': self.is_admin
        })
        return user_dict

    def update(self, data):
        """Update user attributes"""
        super().update(data)
        self.validate()
