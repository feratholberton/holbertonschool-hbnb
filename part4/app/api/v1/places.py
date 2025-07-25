from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True, description='Place title'),
    'description': fields.String(required=True, description='Place description'),
    'price': fields.Float(required=True, description='Place price per night'),
    'latitude': fields.Float(required=True, description='Latitude'),
    'longitude': fields.Float(required=True, description='Longitude'),
    'amenity_ids': fields.List(fields.String, required=False, description='List of Amenity IDs')
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place successfully created')
    @api.response(400, 'Invalid input')
    @jwt_required()
    def post(self):
        """Create a new place"""
        try:
            place_data = api.payload
            user_id = get_jwt_identity()
            user = facade.get_user(user_id)
            place_data['user_id'] = user.id
            new_place = facade.create_place(place_data)
            return new_place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved')
    def get(self):
        """Get all places"""
        places = facade.get_all_places()
        return [place.to_dict() for place in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Get place by ID"""
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated successfully')
    @api.response(400, 'Invalid input or validation error')
    @api.response(404, 'Place not found')
    @api.response(403, 'Unauthorized')
    @jwt_required()
    def put(self, place_id):
        """Update place by ID"""
        user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        user = facade.get_user(user_id)
        place = facade.get_place(place_id)

        if not place:
            return {'error': 'Place not found'}, 404

        if not is_admin and place.owner.id != user.id:
            return {'error': 'Unauthorized'}, 403

        try:
            updated_place = facade.update_place(place_id, api.payload)
            return updated_place.to_dict(), 200
        except ValueError as e:
            return {'error': str(e)}, 400

    @api.response(204, 'Place deleted')
    @api.response(403, 'Unauthorized')
    @api.response(404, 'Place not found')
    @jwt_required()
    def delete(self, place_id):
        user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        user = facade.get_user(user_id)

        try:
            result = facade.delete_place(place_id, user, is_admin=is_admin)
            if not result:
                return {'error': 'Place not found'}, 404
            return '', 204
        except ValueError as e:
            return {'error': str(e)}, 403
