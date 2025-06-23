from app.models.Base_Model import BaseModel

class Review(BaseModel):
    def __init__(self, text, rating, place, user):
        super().__init__()
        if not text:
            raise ValueError("The content of the review. Required.")

        if not (1 <= rating <= 5):
            raise ValueError("Rating given to the place, must be between 1 and 5.")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user
        