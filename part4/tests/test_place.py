import unittest
import uuid
from app import create_app
from flask_jwt_extended import create_access_token

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # tu entres dans le contexte application pour pouvoir créer ton token
        with self.app.app_context():
            self.admin_id = "admin-id-for-tests"
            self.admin_token = create_access_token(identity=self.admin_id, additional_claims={"is_admin": True})

        self.admin_headers = {"Authorization": f"Bearer {self.admin_token}"}

        # même chose pour créer user
        self.email = f"place.user.{uuid.uuid4()}@example.com"
        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": self.email,
            "password": "password"
        }, headers=self.admin_headers)

        self.assertIn(user_res.status_code, [201, 400])
        self.user_id = user_res.get_json()["id"]

        # créer un token user pour la suite
        with self.app.app_context():
            self.token = create_access_token(identity=self.user_id)
        self.headers = {"Authorization": f"Bearer {self.token}"}

    def test_create_place_valid(self):
        payload = {
            "title": "Charming Loft",
            "description": "Very cozy loft in Paris",
            "price": 120.5,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "amenities": []
        }
        res = self.client.post('/api/v1/places/', json=payload, headers=self.headers)
        self.assertEqual(res.status_code, 201)
        data = res.get_json()
        self.assertEqual(data["title"], "Charming Loft")


if __name__ == '__main__':
    unittest.main()
