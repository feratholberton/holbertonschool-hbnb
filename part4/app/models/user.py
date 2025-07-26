from app.models.base import BaseModel
from app.extensions import db, bcrypt
from email_validator import validate_email, EmailNotValidError
from sqlalchemy.orm import validates

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), nullable=False, unique=True)
    password = db.Column(db.String(128), nullable=False)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password, is_admin=False):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email  # validated by @validates below
        self.is_admin = is_admin
        self.hash_password(password)

    def hash_password(self, raw_password):
        self.password = bcrypt.generate_password_hash(raw_password).decode('utf-8')

    def set_password(self, raw_password):
        self.hash_password(raw_password)

    def verify_password(self, raw_password):
        return bcrypt.check_password_hash(self.password, raw_password)

    def to_dict(self):
        return {
            "id": self.id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "is_admin": self.is_admin
        }

    def update(self, data):
        if 'password' in data:
            raise ValueError("Password cannot be updated through this method.")
        if 'email' in data:
            raise ValueError("Email cannot be updated through this method.")
        if 'is_admin' in data:
            raise ValueError("Admin status cannot be modified.")

        for field in ['first_name', 'last_name']:
            if field in data:
                setattr(self, field, data[field])

    @validates('email')
    def validate_email_field(self, key, value):
        try:
            validated = validate_email(value, check_deliverability=False)
            return validated.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email format")
