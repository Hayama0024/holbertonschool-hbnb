from flask_restx import Namespace, Resource, fields
from flask import request
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity, get_jwt

api = Namespace('amenities', description='Amenity operations')


amenity_model = api.model('Amenity', {
    'name': fields.String(required=True, description='Name of the amenity')
})

@api.route('/')
class AmenityList(Resource):
    @api.doc(security='Bearer Auth')
    @api.expect(amenity_model)
    @api.response(201, 'Amenity successfully created')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def post(self):
        """ Register a new amenity (admin only) """
        current_claims = get_jwt()
        if not current_claims.get('is_admin'):
            return {'message': 'Admin privileges required'}, 403

        data = request.get_json()
        if not data or 'name' not in data:
            return {'message': 'Name is required'}, 400
        amenity = facade.create_amenity(data)
        return {'id': amenity.id, 'name': amenity.name}, 201

    @api.response(200, 'List of amenities retrieved successfully')
    def get(self):
        """ Retrieve all amenities """
        amenities = facade.get_all_amenities()
        result = [{'id': a.id, 'name': a.name} for a in amenities]
        return result, 200

@api.route('/<string:amenity_id>')
class AmenityResource(Resource):
    @api.response(200, 'Amenity details retrieved successfully')
    @api.response(404, 'Amenity not found')
    def get(self, amenity_id):
        """ Retrieve amenity by ID """
        amenity = facade.get_amenity(amenity_id)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return {'id': amenity.id, 'name': amenity.name}, 200

    @api.doc(security='Bearer Auth')
    @api.expect(amenity_model, validate=True)
    @api.response(404, 'Amenity not found')
    @api.response(400, 'Invalid input data')
    @api.response(403, 'Admin privileges required')
    @jwt_required()
    def put(self, amenity_id):
        """ Update Amenity (admin only) """
        current_claims = get_jwt()
        if not current_claims.get('is_admin'):
            return {'message': 'Admin privileges required'}, 403

        data = request.get_json()
        amenity = facade.update_amenity(amenity_id, data)
        if not amenity:
            return {'message': 'Amenity not found'}, 404
        return {'message': 'Amenity updated successfully'}, 200
