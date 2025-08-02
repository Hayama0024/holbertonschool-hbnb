# app/api/v1/reviews.py
from flask import request
from flask_restx import Namespace, Resource, fields
from flask_jwt_extended import jwt_required, get_jwt_identity
from app.services import facade

api = Namespace('reviews', description='Review operations')

# クライアントが送るのは text, rating, place_id（root POST の場合）
# ※ /places/<place_id>/reviews の POST では body に place_id は不要
review_model = api.model('ReviewCreate', {
    'text': fields.String(required=True, description='Review text'),
    'rating': fields.Integer(required=True, min=0, max=5, description='Rating from 0 to 5'),
    'place_id': fields.String(required=True, description='Place ID for the review'),
})

# 更新時は任意項目（いずれかは必須）
review_update_model = api.model('ReviewUpdate', {
    'text': fields.String(required=False, description='Review text'),
    'rating': fields.Integer(required=False, min=0, max=5, description='Rating from 0 to 5'),
})

# --------------------------------
# /api/v1/reviews ルート
# --------------------------------
@api.route('/')
class ReviewList(Resource):
    @jwt_required()
    @api.expect(review_model)
    @api.response(201, 'Review successfully created')
    @api.response(400, 'Invalid input data')
    def post(self):
        """Register a new review (JWT required)"""
        data = request.get_json() or {}
        user_id = get_jwt_identity()
        if not user_id:
            api.abort(401, "Invalid or missing token")

        # 正規化：comment -> text
        if 'text' not in data and 'comment' in data:
            data['text'] = data['comment']

        # 型/値チェック
        text = data.get('text')
        rating = data.get('rating')
        place_id = data.get('place_id')

        try:
            rating = int(rating)
        except (TypeError, ValueError):
            api.abort(400, "rating must be an integer between 0 and 5")

        if not text or place_id is None or not (0 <= rating <= 5):
            api.abort(400, "Invalid text, rating, or place_id")

        data['user_id'] = user_id

        try:
            review = facade.create_review(data)
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))

    @api.response(200, 'List of reviews retrieved successfully')
    def get(self):
        """
        Retrieve reviews.
        - All reviews: GET /api/v1/reviews
        - Filter by place: GET /api/v1/reviews?place_id=<ID>
        """
        place_id = request.args.get('place_id')
        if place_id:
            try:
                reviews = facade.get_reviews_by_place(place_id)
                return [r.to_dict_get() for r in reviews], 200
            except ValueError as e:
                api.abort(404, str(e))
        reviews = facade.get_all_reviews()
        return [r.to_dict_get() for r in reviews], 200


# --------------------------------
# /api/v1/reviews/<review_id>
# --------------------------------
@api.route('/<string:review_id>')
class ReviewResource(Resource):
    @api.response(200, 'Review details retrieved successfully')
    @api.response(404, 'Review not found')
    def get(self, review_id):
        """Get one review by ID"""
        try:
            review = facade.get_review(review_id)
            return review.to_dict(), 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(review_update_model)
    @api.response(200, 'Review updated successfully')
    @api.response(400, 'Invalid input data')
    @api.response(404, 'Review not found')
    def put(self, review_id):
        """Update a review (JWT required)"""
        data = request.get_json() or {}

        # 何も変更項目が無い場合はエラー
        if 'text' not in data and 'rating' not in data:
            api.abort(400, "No updatable fields provided (text or rating required)")

        # rating が来ていれば検証
        if 'rating' in data:
            try:
                rating = int(data['rating'])
            except (TypeError, ValueError):
                api.abort(400, "rating must be an integer between 0 and 5")
            if not (0 <= rating <= 5):
                api.abort(400, "rating must be between 0 and 5")

        try:
            facade.update_review(review_id, data)
            return {"message": "Review updated successfully"}, 200
        except ValueError as e:
            msg = str(e)
            if 'not found' in msg.lower():
                api.abort(404, msg)
            api.abort(400, msg)

    @jwt_required()
    @api.response(200, 'Review deleted successfully')
    @api.response(404, 'Review not found')
    def delete(self, review_id):
        """Delete a review (JWT required)"""
        try:
            facade.delete_review(review_id)
            return {"message": "Review deleted successfully"}, 200
        except ValueError as e:
            api.abort(404, str(e))


# --------------------------------
# 互換用：/api/v1/reviews/places/<place_id>/reviews
# GET は既存通り。POST を追加（フロントがこのパスに送る想定）
# --------------------------------
@api.route('/places/<string:place_id>/reviews')
class PlaceReviewList(Resource):
    @api.response(200, 'List of reviews for the place retrieved successfully')
    @api.response(404, 'Place not found')
    def get(self, place_id):
        """Retrieve reviews by place ID (compat endpoint)"""
        try:
            reviews = facade.get_reviews_by_place(place_id)
            return [r.to_dict_get() for r in reviews], 200
        except ValueError as e:
            api.abort(404, str(e))

    @jwt_required()
    @api.expect(api.model('ReviewCreateForPlace', {
        'text': fields.String(required=True, description='Review text'),
        'rating': fields.Integer(required=True, min=0, max=5, description='Rating from 0 to 5'),
    }))
    @api.response(201, 'Review created')
    @api.response(400, 'Invalid input data')
    @api.response(401, 'Unauthorized')
    def post(self, place_id):
        """
        Create a review for a place (JWT required)
        Body: { "text": "...", "rating": 0-5 }
        """
        payload = request.get_json() or {}
        user_id = get_jwt_identity()
        if not user_id:
            api.abort(401, "Invalid or missing token")

        # 正規化
        text = payload.get('text') or payload.get('comment')
        rating = payload.get('rating')

        try:
            rating = int(rating)
        except (TypeError, ValueError):
            api.abort(400, "rating must be an integer between 0 and 5")

        if not text or not (0 <= rating <= 5):
            api.abort(400, "Invalid text or rating")

        try:
            review = facade.create_review({
                'place_id': place_id,
                'user_id': user_id,
                'text': text,
                'rating': rating
            })
            return review.to_dict(), 201
        except ValueError as e:
            api.abort(400, str(e))
