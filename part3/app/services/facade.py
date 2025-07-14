from app.persistence.repository import InMemoryRepository
from app.persistence.repository import SQLAlchemyRepository
from app.models.user import User
from app.models.amenity import Amenity
from app.models.place import Place
from app.models.review import Review


class HBnBFacade:
    def __init__(self):
        self.user_repo = SQLAlchemyRepository(User)
        self.amenity_repo = InMemoryRepository()
        self.place_repo = InMemoryRepository()
        self.review_repo = InMemoryRepository()

    # User Methods -----------------------------------------------------------
    def create_user(self, user_data):
        if self.user_repo.get_by_attribute("email", user_data["email"]):
            raise ValueError("Email already exists")

        user = User()
        user.first_name=user_data["first_name"]
        user.last_name=user_data["last_name"]
        user.email=user_data["email"]
        user.is_admin=user_data.get("is_admin", False)

        user.hash_password(user_data["password"])
        self.user_repo.add(user)
        return user

    def get_user(self, user_id):
        return self.user_repo.get(user_id)

    def get_user_by_email(self, email):
        return self.user_repo.get_by_attribute('email', email)

    def get_all_users(self):
        return self.user_repo.get_all()

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
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

        # Convert amenity IDs to Amenity instances
        amenity_objs = []
        for amenity_id in place_data.get('amenities', []):
            amenity = self.amenity_repo.get(amenity_id)
            if not amenity:
                raise ValueError(f"Amenity with ID {amenity_id} not found")
            amenity_objs.append(amenity)

        place = Place(
            title=place_data['title'],
            description=place_data.get('description', ''),
            price=place_data['price'],
            latitude=place_data['latitude'],
            longitude=place_data['longitude'],
            owner=owner
        )

        for amenity in amenity_objs:
            place.add_amenity(amenity)

        if 'amenity_ids' in place_data:
            if not isinstance(place_data['amenity_ids'], list):
                raise ValueError("Amenities must be a list of amenity IDs")

            for amenity_id in place_data['amenity_ids']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                place.add_amenity(amenity)

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

        # Update fields
        place.update(place_data)

        # Handle owner update
        if 'user_id' in place_data:
            new_owner = self.user_repo.get(place_data['user_id'])
            if not new_owner:
                raise ValueError("Owner not found")
            place.owner = new_owner

        # Handle amenities update
        if 'amenity_ids' in place_data:
            if not isinstance(place_data['amenity_ids'], list):
                raise ValueError("Amenities must be a list of amenity IDs")

            place.amenities = []

            for amenity_id in place_data['amenity_ids']:
                amenity = self.amenity_repo.get(amenity_id)
                if not amenity:
                    raise ValueError(f"Amenity with ID {amenity_id} not found")
                place.add_amenity(amenity)

        return place

    # Review Methods -------------------------------------------------------
    def create_review(self, review_data):
        user = self.get_user(review_data['user_id'])
        if not user:
            raise ValueError('User not found')

        place = self.get_place(review_data['place_id'])
        if not place:
            raise ValueError('Place not found')

        rating = review_data['rating']
        if not (1 <= rating <= 5):
            raise ValueError('Rating must be between 1 and 5')

        new_review = Review(
            text=review_data['text'],
            rating=rating,
            user=user,
            place=place
        )

        place.add_review(new_review)
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

        # Only allow text and rating to be updated
        allowed_fields = {
            'text': review_data.get('text', review.text),
            'rating': review_data.get('rating', review.rating)
        }

        review.update(allowed_fields)
        return review

    def delete_review(self, review_id):
        review = self.get_review(review_id)
        if not review:
            return None

        review.place.reviews = [r for r in review.place.reviews if r.id != review.id]
        self.review_repo.delete(review_id)
        return True
