from app.persistence.repository import InMemoryRepository
from app.models.user import User

class HBnBFacade:
    def __init__(self):
        self.user_repo = InMemoryRepository()
    
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

    def update_user(self, user_id, data):
        user = self.get_user(user_id)
        if not user:
            return None
        user.update(data)
        return user


    # Amenities Methods -------------------------------------------------------
    
    def create_amenity(self, amenity_data):
    # Placeholder for logic to create an amenity
        pass

    def get_amenity(self, amenity_id):
    # Placeholder for logic to retrieve an amenity by ID
        pass

    def get_all_amenities(self):
    # Placeholder for logic to retrieve all amenities
        pass

    def update_amenity(self, amenity_id, amenity_data):
    # Placeholder for logic to update an amenity
        pass
    
    # Reviews Methods ----------------------------------------------------------
    
    def create_review(self, review_data):
        # Placeholder for logic to create a review, including validation for user_id, place_id, and rating
        pass

    def get_review(self, review_id):
        # Placeholder for logic to retrieve a review by ID
        pass

    def get_all_reviews(self):
        # Placeholder for logic to retrieve all reviews
        pass

    def get_reviews_by_place(self, place_id):
        # Placeholder for logic to retrieve all reviews for a specific place
        pass

    def update_review(self, review_id, review_data):
        # Placeholder for logic to update a review
        pass

    def delete_review(self, review_id):
        # Placeholder for logic to delete a review
        pass