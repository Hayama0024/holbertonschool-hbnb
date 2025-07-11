from flask_restx import Namespace, Resource, fields
from flask import request
from flask_jwt_extended import jwt_required, get_jwt, create_access_token
from app.services import facade
from app import bcrypt

api = Namespace('auth', description='Authentication and admin operations')

# Model for user creation
user_model = api.model('User', {
    'first_name': fields.String(required=True, description='First name'),
    'last_name': fields.String(required=True, description='Last name'),
    'email': fields.String(required=True, description='Email address'),
    'password': fields.String(required=True, description='Password'),
    'is_admin': fields.Boolean(required=False, default=False, description='Is Admin')
})

# Model for login
login_model = api.model('Login', {
    'email': fields.String(required=True, description='User email'),
    'password': fields.String(required=True, description='User password')
})

@api.route('/users')
class AdminUserCreate(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(user_model, validate=True)
    @api.response(201, 'User created successfully')
    @api.response(400, 'Invalid input')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """Create a new user (admin only)"""
        claims = get_jwt()
        if not claims.get('is_admin'):
            return {'message': 'Admin privileges required'}, 403

        data = request.get_json()
        if not data:
            return {'message': 'Missing data'}, 400

        hashed_pw = bcrypt.generate_password_hash(data['password']).decode('utf-8')
        user_data = {
            'first_name': data['first_name'],
            'last_name': data['last_name'],
            'email': data['email'],
            'password': hashed_pw,
            'hashed': True
        }

        user = facade.create_user(user_data)
        user.is_admin = data.get('is_admin', False)
        facade.save_user(user)

        return {'message': f"User {user.email} created"}, 201


@api.route('/login')
class Login(Resource):
    @api.expect(login_model)
    @api.response(200, 'Token generated successfully')
    @api.response(401, 'Invalid credentials')
    def post(self):
        """Authenticate user and return a JWT"""
        data = request.get_json()
        user = facade.get_user_by_email(data.get("email"))

        if not user or not bcrypt.check_password_hash(user.password, data.get("password")):
            return {"msg": "Invalid credentials"}, 401

        access_token = create_access_token(
            identity=user.id,
            additional_claims={"is_admin": user.is_admin}
        )

        return {"access_token": access_token}, 200
