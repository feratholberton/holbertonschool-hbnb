import re
from app.models.Base_Model import BaseModel
from app.extensions import bcrypt

class User(BaseModel):
    def __init__(self, first_name, last_name, email, password=None, is_admin=False):
        super().__init__()
        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first name")

        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last name")

        if not re.match(r"[^@]+@[^@]+\.[^@]+", email):
            raise ValueError("Invalid email format")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = is_admin

        self.places = []
        self.reviews = []

        if password:
            self.hash_password(password)

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)