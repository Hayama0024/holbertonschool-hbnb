import unittest
import uuid
from app import create_app
from flask_jwt_extended import create_access_token

class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        with self.app.app_context():
            self.admin_id = f"admin-{uuid.uuid4()}"
            self.admin_token = create_access_token(identity=self.admin_id, additional_claims={"is_admin": True})
        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

        # Crée un user unique
        self.email = f"review.user.{uuid.uuid4()}@example.com"
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "ReviewTest",
            "last_name": "User",
            "email": self.email,
            "password": "test123"
        }, headers=self.admin_headers)
        self.assertIn(user_res.status_code, [201, 400])
        self.user_id = user_res.get_json()["id"]

        # Crée un token pour cet utilisateur
        with self.app.app_context():
            self.token = create_access_token(identity=self.user_id)
        self.headers = {"Authorization": f"Bearer {self.token}"}

        # Crée un place pour pouvoir faire la review
        place_payload = {
            "title": "Test Place",
            "description": "Simple description",
            "price": 100,
            "latitude": 48.85,
            "longitude": 2.35,
            "amenities": []
        }
        place_res = self.client.post('/api/v1/places/', json=place_payload, headers=self.headers)
        self.assertEqual(place_res.status_code, 201)
        self.place_id = place_res.get_json()["id"]

    def test_create_review_valid(self):
        payload = {
            "text": "Very nice!",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 5
        }
        res = self.client.post('/api/v1/reviews/', json=payload, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["text"], "Very nice!")

    def test_get_review_not_found(self):
        res = self.client.get('/api/v1/reviews/nonexistent-id', headers=self.headers)
        self.assertEqual(res.status_code, 404)

if __name__ == '__main__':
    unittest.main()
