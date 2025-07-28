from app.models.base import BaseModel
from app.extensions import db
from sqlalchemy.orm import validates

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.Text, nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    user = db.relationship("User", backref="reviews")

    place_id = db.Column(db.String(60), db.ForeignKey('places.id'), nullable=False)
    place = db.relationship("Place", backref="reviews")

    def __init__(self, text, rating, user_id, place_id):
        super().__init__()
        self.text = text
        self.rating = rating
        self.user_id = user_id
        self.place_id = place_id

    @validates('rating')
    def validate_rating(self, key, value):
        if not (1 <= value <= 5):
            raise ValueError("Rating must be between 1 and 5")
        return value

    @validates('text')
    def validate_text(self, key, value):
        if not value.strip():
            raise ValueError("Review text cannot be empty")
        return value

    def to_dict(self):
        return {
            "id": self.id,
            "text": self.text,
            "rating": self.rating,
            "user": self.user.to_dict() if self.user else None,
            "place_id": self.place_id
        }

    def update(self, data):
        if "rating" in data:
            self.rating = data["rating"]
        if "text" in data:
            self.text = data["text"]
        self.save()
