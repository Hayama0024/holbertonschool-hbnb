import unittest
import uuid
from app import create_app

class TestReview(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        # Création d’un utilisateur avec un email unique
        self.email = f"review.user.{uuid.uuid4()}@example.com"
        user_payload = {
            "first_name": "ReviewTest",
            "last_name": "User",
            "email": self.email
        }
        user_res = self.client.post('/api/v1/users/', json=user_payload)
        self.assertEqual(user_res.status_code, 201)
        self.user_id = user_res.get_json()["id"]

        # Création d’un lieu avec 'title' et 'owner_id'
        place_payload = {
            "title": "ReviewTest Place",
            "price": 100,
            "latitude": 48.85,
            "longitude": 2.35,
            "owner_id": self.user_id
        }
        place_res = self.client.post('/api/v1/places/', json=place_payload)
        self.assertEqual(place_res.status_code, 201)
        self.place_id = place_res.get_json()["id"]

    def tearDown(self):
        self.client.delete(f'/api/v1/users/{self.user_id}')
        self.client.delete(f'/api/v1/places/{self.place_id}')

    def test_create_review_valid(self):
        payload = {
            "text": "Very nice!",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 5
        }
        res = self.client.post('/api/v1/reviews/', json=payload)
        self.assertEqual(res.status_code, 201)
        self.assertEqual(res.get_json()["text"], "Very nice!")

    def test_get_review_by_id(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Great spot!",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 4
        })
        self.assertEqual(res.status_code, 201)
        review_id = res.get_json()["id"]

        get_res = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["text"], "Great spot!")

    def test_update_review_valid(self):
        res = self.client.post('/api/v1/reviews/', json={
            "text": "Okay.",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 3
        })
        self.assertEqual(res.status_code, 201)
        review_id = res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/reviews/{review_id}', json={
            "text": "Actually, excellent!",
            "user_id": self.user_id,
            "place_id": self.place_id,
            "rating": 5
        })
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["message"], "Review updated successfully")

        get_res = self.client.get(f'/api/v1/reviews/{review_id}')
        self.assertEqual(get_res.status_code, 200)
        updated_data = get_res.get_json()
        self.assertEqual(updated_data["text"], "Actually, excellent!")
        self.assertEqual(updated_data["rating"], 5)


    def test_get_review_not_found(self):
        res = self.client.get('/api/v1/reviews/nonexistent-id-123')
        self.assertEqual(res.status_code, 404)


if __name__ == '__main__':
    unittest.main()
