from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade
from flask_jwt_extended import jwt_required, get_jwt_identity

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=0, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})


@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """ Register a new Review """
        data = request.json
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """ Retrieve all review """
        reviews = facade.get_all_reviews()
        return [r.to_dict_get() for r in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """ Retrieve a review by review_ID """
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_model)
    @api.response(200, 'Review updated successfully')
    @api.response(404, 'Review not found')
    @api.response(400, 'Invalid input data')
    def put(self, review_id):
        """ Update review """
        data = request.json
        try:
            updated = facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """ Delete review """
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(404, str(e))


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """ Retrieve a review by place ID """
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [r.to_dict_get() for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
