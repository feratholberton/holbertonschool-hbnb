#!/usr/bin/python3
from Base_Model import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        if not title or len(title) > 100:
            raise ValueError("too many characters!")
        if price < 0:
                raise ValueError("cannot be negative")
        if not (-90 <= latitude <= 90):
            raise ValueError("incorrect latitude")
        if not(-180 <= longitude <= 180):
             raise ValueError("incorrect length")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User")
        
        self.id = id
        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
