from app.models.base import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.description = description or ""
        self.owner = owner
        self.reviews = []
        self.amenities = []

    @property
    def title(self):
        return self._title

    @title.setter
    def title(self, value):
        if not value or len(value) > 100:
            raise ValueError("Title is required and must be <= 100 characters.")
        self._title = value

    @property
    def price(self):
        return self._price

    @price.setter
    def price(self, value):
        if value <= 0:
            raise ValueError("Price must be positive.")
        self._price = value

    @property
    def latitude(self):
        return self._latitude

    @latitude.setter
    def latitude(self, value):
        if not -90.0 <= value <= 90.0:
            raise ValueError("Latitude out of bounds.")
        self._latitude = value

    @property
    def longitude(self):
        return self._longitude

    @longitude.setter
    def longitude(self, value):
        if not -180.0 <= value <= 180.0:
            raise ValueError("Longitude out of bounds.")
        self._longitude = value

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            "id": self.id,
            "title": self.title,
            "description": self.description,
            "price": self.price,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "owner": self.owner.to_dict() if hasattr(self.owner, "to_dict") else str(self.owner),
            "amenities": [amenity.to_dict() for amenity in self.amenities],
            "reviews": [review.to_dict() for review in self.reviews]
        }

    def update(self, data):
        for field in ['title', 'description', 'price', 'latitude', 'longitude']:
            if field in data:
                setattr(self, field, data[field])
        self.save()
