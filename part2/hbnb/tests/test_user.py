import unittest
from app import create_app

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_get_user_by_id(self):
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Léo",
            "last_name": "Salin",
            "email": "leo.salins@example.com"
        })
        self.assertEqual(post_res.status_code, 201)
        user_id = post_res.get_json()["id"]

        get_res = self.client.get(f'/api/v1/users/{user_id}')
        self.assertEqual(get_res.status_code, 200)
        self.assertEqual(get_res.get_json()["email"], "leo.salins@example.com")

    def test_update_user_valid(self):
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Anna",
            "last_name": "Dupont",
            "email": "anna@example.com"
        })
        user_id = post_res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Anna-Marie",
            "last_name": "Dupont",
            "email": "anna.dupont@example.com"
        })

        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["first_name"], "Anna-Marie")

if __name__ == '__main__':
    unittest.main()
