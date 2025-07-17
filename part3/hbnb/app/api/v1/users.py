from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('users', description='User operations')

user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user')
})

@api.route('/')
class UserList(Resource):
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Email already registered')
    def post(self):
        data = request.get_json()
        if facade.get_user_by_email(data.get("email")):
            return {"error": "Email already registered"}, 400
        user = facade.create_user(data)
        return user.to_dict(), 201

@api.route('/<string:user_id>')
class UserProfile(Resource):
    @api.response(200, 'User retrieved successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    def get(self, user_id):
        user = facade.get_user(user_id)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.expect(user_model, validate=True)
    @api.response(200, 'Profile updated successfully')
    @api.response(403, 'Not authorized')
    @api.response(404, 'User not found')
    @jwt_required()
    def put(self, user_id):
        """Update own profile"""
        identity = get_jwt_identity()
        if identity != user_id:
            return {"error": "Not authorized"}, 403
        user = facade.update_user(user_id, api.payload)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200
