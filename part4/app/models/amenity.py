from app.models.base import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(50), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()
        self.name = name

    @validates('name')
    def validate_name(self, key, value):
        if not value or len(value.strip()) == 0:
            raise ValueError("Amenity name is required")
        if len(value) > 50:
            raise ValueError("Amenity name must not exceed 50 characters")
        return value.strip()

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def update(self, data):
        if 'name' in data:
            self.name = data['name']
        self.save()
