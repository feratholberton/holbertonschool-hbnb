from app.models.Base_Model import BaseModel
from app.models.place import Place
from app.models.user import User

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("The content of the review. Required.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating given to the place, must be between 1 and 5.")

        if not isinstance(place, Place):
            raise ValueError("Invalid place")

        if not isinstance(user, User):
            raise ValueError("invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

        place.reviews.append(self)
