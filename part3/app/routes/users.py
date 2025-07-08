from flask import Blueprint, request, jsonify, abort
from app.facade.user_facade import UserFacade

user_bp = Blueprint('user_bp', __name__)
user_facade = UserFacade()

@user_bp.route('/', methods=['GET'])
def get_all_users():
    users = user_facade.get_all_users()
    return jsonify([user.to_dict() for user in users]), 200

@user_bp.route('/', methods=['POST'])
def create_user():
    data = request.get_json()
    if not data or 'email' not in data or 'password' not in data:
        abort(400, description="Missing email or password")
    try:
        user = user_facade.create_user(data)
        return jsonify(user.to_dict()), 201
    except ValueError as e:
        abort(400, description=str(e))

@user_bp.route('/<user_id>', methods=['GET'])
def get_user(user_id):
    user = user_facade.get_user_by_id(user_id)
    if not user:
        abort(404, description="User not found")
    return jsonify(user.to_dict()), 200

@user_bp.route('/<user_id>', methods=['PUT'])
def update_user(user_id):
    data = request.get_json()
    if not data:
        abort(400, description="No data provided")
    try:
        user = user_facade.update_user(user_id, data)
        if not user:
            abort(404, description="User not found")
        return jsonify(user.to_dict()), 200
    except ValueError as e:
        abort(400, description=str(e))

@user_bp.route('/<user_id>', methods=['DELETE'])
def delete_user(user_id):
    success = user_facade.delete_user(user_id)
    if not success:
        abort(404, description="User not found")
    return jsonify({"message": "User deleted successfully"}), 200
