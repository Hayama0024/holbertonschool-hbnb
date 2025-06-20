import unittest
from app import create_app

class TestAmenity(unittest.TestCase):

    def setUp(self):
        app = create_app()
        app.testing = True
        self.client = app.test_client()

    def test_get_amenity_by_id(self):
        res = self.client.post('/api/v1/amenities/', json={"name": "Climatisation"})
        amenity_id = res.get_json()["id"]

        get_res = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["name"], "Climatisation")

    def test_update_amenity_valid(self):
        # Création d'une amenity
        res = self.client.post('/api/v1/amenities/', json={"name": "Jacuzzi"})
        amenity_id = res.get_json()["id"]

        # Mise à jour de l'amenity
        put_res = self.client.put(f'/api/v1/amenities/{amenity_id}', json={"name": "Jacuzzi Luxe"})
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["message"], "Amenity updated successfully")

        # Vérification du changement via GET
        get_res = self.client.get(f'/api/v1/amenities/{amenity_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["name"], "Jacuzzi Luxe")


if __name__ == '__main__':
    unittest.main()
