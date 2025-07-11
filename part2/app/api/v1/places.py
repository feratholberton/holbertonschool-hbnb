from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('places', description='Place operations')

place_model = api.model('Place', {
    'title': fields.String(required=True),
    'description': fields.String,
    'price': fields.Float(required=True),
    'latitude': fields.Float(required=True),
    'longitude': fields.Float(required=True),
    'owner_id': fields.String(required=True),
    'amenities': fields.List(fields.String, required=True)
})

@api.route('/')
class PlaceList(Resource):
    @api.expect(place_model, validate=True)
    @api.response(201, 'Place created')
    @api.response(400, 'Bad Request')
    def post(self):
        """Create a new place"""
        try:
            data = api.payload
            place = facade.create_place(data)
            return place.to_dict(), 201
        except ValueError as e:
            return {"error": str(e)}, 400

    @api.response(200, 'List of places retrieved')
    def get(self):
        places = facade.get_all_places()
        return [p.to_dict() for p in places], 200

@api.route('/<place_id>')
class PlaceResource(Resource):
    @api.response(200, 'Place details')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        place = facade.get_place(place_id)
        if not place:
            return {"error": "Place not found"}, 404
        return place.to_dict(), 200

    @api.expect(place_model, validate=True)
    @api.response(200, 'Place updated')
    @api.response(404, 'Place not found')
    @api.response(400, 'Invalid input data')
    def put(self, place_id):
        """Update a place"""
        place_data = api.payload
        updated = facade.update_place(place_id, place_data)
        if not updated:
            return {'error': 'Place not found'}, 404
        return updated.to_dict(), 200
