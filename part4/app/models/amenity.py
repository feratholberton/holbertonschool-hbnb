from app.models.base import BaseModel

class Amenity(BaseModel):
    def __init__(self, name):
        super().__init__()
        self.name = name

    @property
    def name(self):
        return self._name

    @name.setter
    def name(self, value):
        if not value or len(value) > 50:
            raise ValueError("Amenity name is required and must not exceed 50 characters")
        self._name = value

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }

    def update(self, data):
        if 'name' in data:
            self.name = data['name']
        self.save()