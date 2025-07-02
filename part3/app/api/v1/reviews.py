from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

# Define the review model for input validation and documentation
review_model = api.model('Review', {
    'text': fields.String(required=True, description='Text of the review'),
    'rating': fields.Integer(required=True, description='Rating of the place (1-5)'),
    'user_id': fields.String(required=True, description='ID of the user'),
    'place_id': fields.String(required=True, description='ID of the place')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review"""
        review_data = api.payload
        try:
            new_review = facade.create_review(review_data)
            return {
                'review_id': new_review.id,
                'text': new_review.text,
                'rating': new_review.rating,
                'user_id': new_review.user,
                'place_id': new_review.place
            }, 201
        except ValueError as error:
            if str(error) == 'User not found':
                return {'error': 'User not found'}, 404
            
            if str(error) == 'Place not found':
                return {'error': 'Place not found'}, 404
            
            if str(error) == 'Rating must be a number between 1 and 5, inclusive':
                return {'error': 'Rating must be a number between 1 and 5, inclusive'}, 400

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """Retrieve a list of all reviews"""
        reviews = facade.get_all_reviews()
        return [
            {
                'text': review.text,
                'rating': review.rating,
                'place_id': review.place,
                'user_id': review.user
            } for review in reviews
        ], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review details by ID"""
        if not facade.get_review(review_id):
            return {'error': 'Review not found'}, 404
        
        review = facade.get_review(review_id)  
        return {
            'text': review.text,
            'rating': review.rating,
            'place_id': review.place,
            'user_id': review.user
        }, 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """Update a review's information"""
        try:
            up_review_data = api.payload
            facade.update_review(review_id, up_review_data)
            return {'Success': 'Review updated successfully'}, 200
        except ValueError as error:
            if str(error) == 'Review not found':
                return {'error': 'Review not found'}, 404
            elif str(error) == 'User not found':
                return {'error': 'User not found'}, 404
            elif str(error) == 'Place not found':
                return {'error': 'Place not found'}, 404
            else:
                return {'error': 'Rating must be a number between 1 and 5, inclusive'}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review"""
        try:
            facade.delete_review(review_id)
            return {'Success:': 'Review deleted successfully'}, 200
        except ValueError:
            return {'error': 'review not found'}, 404

@api.route('/places/<place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews for a specific place"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [
                {
                    'text': review.text,
                    'rating': review.rating,
                    'place_id': review.place,
                    'user_id': review.user
                } for review in reviews
            ], 200
        except ValueError:
            return {'error': 'Place not found'}, 404