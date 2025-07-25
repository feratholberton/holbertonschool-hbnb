from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt
from app.services import facade

api = Namespace('users', description='User operations')

# Define the user model for input validation and documentation
# User model for creation (includes password and is_admin)
user_create_model = api.model('UserCreate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='User password', min_length=6),
    'is_admin': fields.Boolean(required=False, default=False, description='Is the user an admin?')
})

# User model for update (excludes password and is_admin)
user_update_model = api.model('UserUpdate', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=False, description='Email of the user'),
    'password': fields.String(required=False, description='User password', min_length=6)
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_create_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @jwt_required()
    def post(self):
        """Create new user"""
        is_admin = get_jwt().get("is_admin", False)
        
        if not is_admin:
            return {'error': 'Admin privileges required'}, 403

        user_data = api.payload
        existing_user = facade.get_user_by_email(user_data['email'])
        if existing_user:
            return {'error': 'Email already registered'}, 400

        new_user = facade.create_user(user_data)
        return new_user.to_dict(), 201

    @api.response(200, 'List of users retrieved')
    def get(self):
        """Get all users"""
        users = facade.get_all_users()
        return [ user.to_dict() for user in users ], 200

@api.route('/<user_id>')
class UserResource(Resource):
    @api.response(200, 'User details retrieved successfully')
    @api.response(404, 'User not found')
    def get(self, user_id):
        """Get user by ID"""
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200

    @api.expect(user_update_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid input')
    @api.response(401, 'Missing or invalid token')
    @api.response(403, 'Unauthorized — can only update your own account')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update user by ID"""
        current_user_id = get_jwt_identity()
        is_admin = get_jwt().get("is_admin", False)

        if not is_admin and current_user_id != user_id:
            return {'error': 'Unauthorized'}, 403

        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404

        data = api.payload

        if not is_admin:
            data.pop("email", None)
            data.pop("password", None)

        if is_admin and "email" in data:
            existing_user = facade.get_user_by_email(data["email"])
            if existing_user and existing_user.id != user_id:
                return {'error': 'Email already in use'}, 400

        try:
            allow_email_change = is_admin
            allow_password_change = is_admin

            updated_user = facade.update_user(
                user_id, data,
                allow_email_change=allow_email_change,
                allow_password_change=allow_password_change
            )
            return updated_user.to_dict(), 200
        except ValueError as error:
            return {'error': str(error)}, 400

@api.route('/email/<string:email>')
class UserByEmailResource(Resource):
    @api.response(200, 'User found')
    @api.response(404, 'User not found')
    def get(self, email):
        """Get user by email address"""
        user = facade.get_user_by_email(email)
        if not user:
            return {'error': 'User not found'}, 404
        return user.to_dict(), 200
