from flask_restx import Namespace, Resource
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('protected', description='Protected operations')

@api.route('/protected')
class Protected(Resource):
    @jwt_required()
    def get(self):
        user_id = get_jwt_identity()
        claims = get_jwt()
        return {
            "message": f"Hello {user_id} - admin: {claims['is_admin']}"
        }, 200
