from app.models.Base_Model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=None):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("Title is required and must be <= 100 characters.")
        if price <= 0:
            raise ValueError("Price must be positive.")
        if not -90.0 <= latitude <= 90.0:
            raise ValueError("Latitude out of bounds.")
        if not -180.0 <= longitude <= 180.0:
            raise ValueError("Longitude out of bounds.")

        self.title = title
        self.description = description or ""
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner  # should be an instance of User
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)