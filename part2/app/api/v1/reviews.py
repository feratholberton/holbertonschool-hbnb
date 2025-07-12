from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, description='Rating from 1 to 5'),
    'user_id': fields.String(required=True, description='ID of the user leaving the review'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input or entity not found')
    def post(self):
        try:
            review_data = api.payload
            new_review = facade.create_review(review_data)
            return new_review.to_dict(), 201
        except ValueError as error:
            return {'error': str(error)}, 400

    @api.response(200, 'List of reviews retrieved')
    def get(self):
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        review = facade.get_review(review_id)
        if not review:
            return {'error': 'Review not found'}, 404
        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input')
    def put(self, review_id):
        try:
            updated = facade.update_review(review_id, api.payload)
            if not updated:
                return {'error': 'Review not found'}, 404
            return updated.to_dict(), 200
        except ValueError as error:
            return {'error': str(error)}, 400

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        deleted = facade.delete_review(review_id)
        if not deleted:
            return {'error': 'Review not found'}, 404
        return {'success': 'Review deleted successfully'}, 200

@api.route('/places/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'List of reviews for place retrieved')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        reviews = facade.get_reviews_by_place(place_id)
        if reviews is None:
            return {'error': 'Place not found'}, 404
        return [review.to_dict() for review in reviews], 200
