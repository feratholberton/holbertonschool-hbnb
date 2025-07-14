from app.models.base import BaseModel
from email_validator import validate_email, EmailNotValidError
from flask_bcrypt import generate_password_hash, check_password_hash
from app.extensions import db

class User(BaseModel):
    __tablename__ = 'users'

    _first_name = db.Column('first_name',db.String(50), nullable=False)
    _last_name = db.Column('last_name',db.String(50), nullable=False)
    _email = db.Column('email',db.String(120), nullable=False, unique=True)
    _password = db.Column('password',db.String(128), nullable=False)
    _is_admin = db.Column('is_admin',db.Boolean, default=False)


    @property
    def first_name(self):
        return self._first_name

    @first_name.setter
    def first_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("First name is required and cannot exceed 50 characters")
        self._first_name = value

    @property
    def last_name(self):
        return self._last_name

    @last_name.setter
    def last_name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Last name is required and cannot exceed 50 characters")
        self._last_name = value

    @property
    def email(self):
        return self._email

    @email.setter
    def email(self, value):
        try:
            email_validation = validate_email(value, check_deliverability=False)
            self._email = email_validation.normalized
        except EmailNotValidError:
            raise ValueError("Invalid email format")

    def hash_password(self, password):
        """Hashes the password before storing it."""
        self._password = generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        """Verifies if the provided password matches the hashed password."""
        return check_password_hash(self._password, password)

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
        self.save()
