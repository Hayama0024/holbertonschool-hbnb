import unittest
from app import create_app
from app.api.v1.places import facade
from app.models.user import User
from app.persistence.repository import InMemoryRepository, AmenityRepository

class TestPlace(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        self.user_repo = facade.user_repository = InMemoryRepository()
        facade.place_repository = InMemoryRepository()
        facade.review_repository = InMemoryRepository()
        facade.amenity_repository = AmenityRepository()

        self.default_user = User("John", "Doe", "john@example.com")
        self.user_repo.save(self.default_user)

    def test_create_place_valid(self):
        res = self.client.post('/api/v1/places/', json={
            "title": "Charming Flat",
            "price": 100,
            "latitude": 48.8566,
            "longitude": 2.3522,
            "owner_id": self.default_user.id,
            "amenities": []
        })
        self.assertEqual(res.status_code, 201)

    def test_create_place_invalid_latitude(self):
        res = self.client.post('/api/v1/places/', json={
            "title": "Bad Latitude",
            "price": 50,
            "latitude": 100,  # invalide
            "longitude": 2.0,
            "owner_id": self.default_user.id,
            "amenities": []
        })
        self.assertEqual(res.status_code, 400)

    def test_create_place_negative_price(self):
        res = self.client.post('/api/v1/places/', json={
            "title": "Cheap place",
            "price": -50,  # invalide
            "latitude": 45,
            "longitude": 1,
            "owner_id": self.default_user.id,
            "amenities": []
        })
        self.assertEqual(res.status_code, 400)

if __name__ == '__main__':
    unittest.main()
