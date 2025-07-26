from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.persistence.user_repository import UserRepository

from app.extensions import db

from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review

class HBnBFacade:
    def __init__(self):
        self.user_repo = UserRepository()
        self.amenity_repo = InMemoryRepository()
        self.place_repo = SQLAlchemyRepository(Place)
        self.review_repo = SQLAlchemyRepository(Review)

    # User Methods -----------------------------------------------------------
    def create_user(self, user_data):
        user = User(**user_data)
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data, allow_email_change=False, allow_password_change=False):
        user = self.user_repo.get(user_id)
        if not user:
            raise ValueError("User not found")

        if "email" in data:
            if not allow_email_change:
                raise ValueError("Email cannot be updated through this method.")
            existing = self.get_user_by_email(data["email"])
            if existing and existing.id != user_id:
                raise ValueError("Email already in use")
            user.email = data["email"]

        if "password" in data:
            if not allow_password_change:
                raise ValueError("Password cannot be updated through this method.")
            user.set_password(data["password"])

        user.first_name = data["first_name"]
        user.last_name = data["last_name"]
        db.session.commit()
        return user

    # Amenities Methods -------------------------------------------------------
    def create_amenity(self, amenity_data):
        amenity = Amenity(**amenity_data)
        self.amenity_repo.add(amenity)
        return amenity

    def get_amenity(self, amenity_id):
        return self.amenity_repo.get(amenity_id)

    def get_all_amenities(self):
        return self.amenity_repo.get_all()

    def update_amenity(self, amenity_id, amenity_data):
        amenity = self.get_amenity(amenity_id)
        if not amenity:
            return None
        amenity.update(amenity_data)
        return amenity

    # Place Methods -------------------------------------------------------
    def create_place(self, place_data):
        owner = self.user_repo.get(place_data['user_id'])
        if not owner:
            raise ValueError("Owner not found")

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner_id=owner.id
        )

        self.place_repo.add(place)
        return place

    def get_place(self, place_id):
        return self.place_repo.get(place_id)

    def get_all_places(self):
        return self.place_repo.get_all()

    def update_place(self, place_id, place_data):
        place = self.get_place(place_id)
        if not place:
            return None

        place.update(place_data)
        db.session.commit() 
        return place

    def delete_place(self, place_id, requesting_user, is_admin=False):
        place = self.get_place(place_id)
        if not place:
            return None

        if not is_admin:
            raise ValueError("Unauthorized")

        self.place_repo.delete(place_id)
        return True

    # Review Methods -------------------------------------------------------
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError('User not found')

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError('Place not found')

        if place.owner_id == user.id:
            raise ValueError("Cannot review your own place")

        existing_review = self.review_repo.get_by_attribute_multiple({
            "user_id": user.id,
            "place_id": place.id
        })
        if existing_review:
            raise ValueError("You have already reviewed this place")

        new_review = Review(
            text=review_data['text'],
            rating=review_data['rating'],
            user_id=user.id,
            place_id=place.id
        )

        self.review_repo.add(new_review)
        return new_review

    def get_review(self, review_id):
        return self.review_repo.get(review_id)

    def get_all_reviews(self):
        return self.review_repo.get_all()
    
    def get_reviews_by_place(self, place_id):
        return [review for review in self.review_repo.get_all() if review.place.id == place_id]

    def update_review(self, review_id, review_data):
        review = self.get_review(review_id)
        if not review:
            return None

        review.update(review_data)
        db.session.commit()
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None

        self.review_repo.delete(review_id)
        return True
