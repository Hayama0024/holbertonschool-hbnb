from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt
from app.services import facade

api = Namespace('admin', description='Admin User operations')

user_model = api.model('Admin', {
    'first_name': fields.String(required=True, description='First name of the user'),
    'last_name': fields.String(required=True, description='Last name of the user'),
    'email': fields.String(required=True, description='Email of the user'),
    'password': fields.String(required=True, description='Password of the user'),
    'is_admin': fields.Boolean(description='Admin status of the user')
})

@api.doc(security='Bearer Auth')
@api.route('/')
class AdminUserList(Resource):
    @api.response(200, 'List of users retrieved successfully')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def get(self):
        """List all users (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        users = facade.get_all_users()
        return [u.to_dict() for u in users], 200

    @api.expect(user_model, validate=True)
    @api.response(201, 'User successfully created')
    @api.response(400, 'Email already registered')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a user (admin only, can set is_admin)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        data = request.get_json()
        if facade.get_user_by_email(data.get("email")):
            return {"error": "Email already registered"}, 400
        user = facade.create_user(data)
        return user.to_dict(), 201

@api.doc(security='Bearer Auth')
@api.route('/<string:user_id>')
class AdminUser(Resource):
    @api.expect(user_model, validate=True)
    @api.response(200, 'User updated successfully')
    @api.response(400, 'Invalid data or duplicate email')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, user_id):
        """Update any user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403

        data = request.get_json()
        if "email" in data:
            existing = facade.get_user_by_email(data["email"])
            if existing and str(existing.id) != user_id:
                return {"error": "Email already in use"}, 400

        user = facade.update_user(user_id, data)
        if not user:
            return {"error": "User not found"}, 404
        return user.to_dict(), 200

    @api.response(200, 'User deleted successfully')
    @api.response(404, 'User not found')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def delete(self, user_id):
        """Delete any user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'error': 'Admin privileges required'}, 403
        user = facade.get_user(user_id)
        if not user:
            return {'error': 'User not found'}, 404
        facade.delete_user(user_id)
        return {"message": "User deleted successfully"}, 200
