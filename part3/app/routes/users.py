from flask import Blueprint, request, jsonify, abort
from app import db
from app.models.user import User

user_bp = Blueprint('user_bp', __name__)

@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = User.query.all()
    return jsonify([user.to_dict() for user in users])

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Missing email or password")
    new_user = User(email=data['email'], password=data['password'])
    db.session.add(new_user)
    db.session.commit()
    return jsonify(new_user.to_dict()), 201

@user_bp.route('/<int:user_id>', methods=['PUT'])
def update_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    data = request.get_json()
    if not data:
        abort(400, description="No data provided")

    if 'email' in data:
        user.email = data['email']
    if 'password' in data:
        user.password = data['password']

    db.session.commit()
    return jsonify(user.to_dict())

@user_bp.route('/<int:user_id>', methods=['DELETE'])
def delete_user(user_id):
    user = User.query.get(user_id)
    if not user:
        abort(404, description="User not found")

    db.session.delete(user)
    db.session.commit()
    return jsonify({'message': 'User deleted successfully'})
