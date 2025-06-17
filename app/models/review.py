#!/usr/bin/python3
from Base_Model import BaseModel
from place import Place
from user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("required text")
        
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        
        if not isinstance(place, Place):
            raise ValueError("Invalid place")
        
        if not isinstance(user, User):
            raise ValueError("invalid user")
        
        
        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
