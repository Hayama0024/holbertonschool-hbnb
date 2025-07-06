from flask import request
from flask_restx import Namespace, Resource, fields
from app.services import facade

api = Namespace('reviews', description='Review operations')

review_model = api.model('Review', {
    'text': fields.String(required=True),
    'rating': fields.Integer(required=True, min=0, max=5),
    'user_id': fields.String(required=True),
    'place_id': fields.String(required=True)
})


@api.route('/')
class ReviewList(Resource):
    @api.expect(review_model)
    def post(self):
        data = request.json
        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    def get(self):
        reviews = facade.get_all_reviews()
        return [r.to_dict_get() for r in reviews], 200


@api.route('/<string:review_id>')
class ReviewResource(Resource):
    def get(self, review_id):
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @api.expect(review_model)
    def put(self, review_id):
        data = request.json
        try:
            updated = facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            api.abort(400, str(e))

    def delete(self, review_id):
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(404, str(e))


@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    def get(self, place_id):
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [r.to_dict_get() for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))
