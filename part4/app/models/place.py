from app.models.base import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates, relationship
from app.models.associations import place_amenity


class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)

    owner_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    owner = db.relationship("User", backref="places")

    amenities = relationship(
        "Amenity",
        secondary=place_amenity,
        backref="places"
    )

    def __init__(self, title, price, latitude, longitude, owner_id, description=None):
        super().__init__()
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.description = description or ""

    @validates('title')
    def validate_title(self, key, value):
        if not value or not value.strip():
            raise ValueError("Title is required and cannot be empty")
        return value

    @validates('price')
    def validate_price(self, key, value):
        if value <= 0:
            raise ValueError("Price must be greater than 0")
        return value

    @validates('latitude')
    def validate_latitude(self, key, value):
        if not (-90 <= value <= 90):
            raise ValueError("Latitude must be between -90 and 90")
        return value

    @validates('longitude')
    def validate_longitude(self, key, value):
        if not (-180 <= value <= 180):
            raise ValueError("Longitude must be between -180 and 180")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner_id": self.owner_id,
            "owner": {
                "first_name": self.owner.first_name,
                "last_name": self.owner.last_name
            } if self.owner else None,
            "amenities": [a.to_dict() for a in self.amenities],
            "reviews": [r.to_dict() for r in self.reviews]
        }

    def update(self, data):
        for field in ['title', 'description', 'price', 'latitude', 'longitude']:
            if field in data:
                setattr(self, field, data[field])
        self.save()
