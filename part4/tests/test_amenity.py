import unittest
from app import create_app
from flask_jwt_extended import create_access_token

class TestAmenity(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()
        self.ctx = app.app_context()
        self.ctx.push()

        # Créer un token admin pour les tests
        self.admin_token = create_access_token(identity="test-admin", additional_claims={"is_admin": True})

    def tearDown(self):
        self.ctx.pop()

    def test_get_amenity_by_id(self):
        res = self.client.post('/api/v1/amenities/',
                               json={"name": "Climatisation"},
                               headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(res.status_code, 201)
        amenity_id = res.get_json()["id"]

        get_res = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["name"], "Climatisation")

    def test_update_amenity_valid(self):
        res = self.client.post('/api/v1/amenities/',
                               json={"name": "Jacuzzi"},
                               headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(res.status_code, 201)
        amenity_id = res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/amenities/{amenity_id}',
                                  json={"name": "Jacuzzi Luxe"},
                                  headers={"Authorization": f"Bearer {self.admin_token}"})
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["message"], "Amenity updated successfully")

        get_res = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["name"], "Jacuzzi Luxe")

if __name__ == '__main__':
    unittest.main()
