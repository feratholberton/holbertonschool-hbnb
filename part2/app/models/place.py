from Base_Model import BaseModel
from user import User

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        super().__init__()
        if not title or len(title) > 100:
            raise ValueError("The title of the place. Required, maximum length of 100 characters.")

        if price < 0:
                raise ValueError("Must be a positive value.")

        if not (-90 <= latitude <= 90):
            raise ValueError("Latitude coordinate for the place location. Must be within the range of -90.0 to 90.0.")

        if not(-180 <= longitude <= 180):
             raise ValueError("Longitude coordinate for the place location. Must be within the range of -180.0 to 180.0.")

        if not isinstance(owner, User):
            raise ValueError("Owner must be a User")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []
        owner.places.append(self)
