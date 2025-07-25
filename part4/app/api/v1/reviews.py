from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=1, max=5, description='Rating from 1 to 5'),
    'place_id': fields.String(required=True, description='ID of the place being reviewed')
})

@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input or entity not found')
    @api.response(401, 'Unauthenticated')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def post(self):
        """Create new review"""
        try:
            review_data = api.payload
            user_id = get_jwt_identity()
            user = facade.get_user(user_id)
            if not user:
                return {'error': 'User not found'}, 404
            place = facade.get_place(review_data['place_id'])
        except ValueError as error:
            return {'error': str(error)}, 400

        if not place:
            return {'error': 'Place not found'}, 404

        if place.owner.id == user.id:
            return {'error': 'Cannot review your own place'}, 403

        for review in facade.get_all_reviews():
            if review.place.id == place.id and review.user.id == user.id:
                return {'error': 'You have already reviewed this place'}, 400

        review_data['user_id'] = user.id
        review = facade.create_review(review_data)
        return review.to_dict(), 201

    @api.response(200, 'List of reviews retrieved')
    def get(self):
        """Get all reviews"""
        reviews = facade.get_all_reviews()
        return [review.to_dict() for review in reviews], 200

@api.route('/<review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review retrieved')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get review by ID"""
        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        return review.to_dict(), 200

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(401, 'Unauthenticated')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'Review not found')
    @jwt_required()
    def put(self, review_id):
        """Update review by ID"""
        try:
            user_id = get_jwt_identity()
            review = facade.get_review(review_id)
            if not review:
                return {'error': 'Review not found'}, 404
        except ValueError as error:
            return {'error': str(error)}, 400

        if review.user.id != user_id:
            return {'error': 'Unauthorized'}, 403

        updated_review = facade.update_review(review_id, api.payload)
        return updated_review.to_dict(), 200

    @api.response(204, 'Review deleted')
    @api.response(401, 'Unauthenticated')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'Review not found')
    @jwt_required()
    def delete(self, review_id):
        """Delete review by ID"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        review = facade.get_review(review_id)

        if not review:
            return {'error': 'Review not found'}, 404

        if not is_admin and review.user.id != user_id:
            return {'error': 'Unauthorized'}, 403

        facade.delete_review(review_id)
        return '', 204

@api.route('/places/<place_id>/reviews')
class PlaceReviews(Resource):
    @api.response(200, 'List of reviews for place retrieved')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get all reviews from Place ID"""
        place = facade.get_place(place_id)
        if not place:
            return {'error': 'Place not found'}, 404

        reviews = facade.get_reviews_by_place(place_id)
        return [review.to_dict() for review in reviews], 200
