import unittest
import uuid
from app import create_app
from app.services import facade

class TestUser(unittest.TestCase):
    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

        login_res = self.client.post('/api/v1/auth/login', json={
            "email": "admin@example.com",
            "password": "adminpassword"
        })
        self.assertEqual(login_res.status_code, 200)
        self.token = login_res.get_json()["access_token"]
        self.headers = {"Authorization": f"Bearer {self.token}"}

        user_res = self.client.post('/api/v1/users/', json={
            "first_name": "Test",
            "last_name": "User",
            "email": "test.user@example.com",
            "password": "pass123"
        }, headers=self.headers)

        if user_res.status_code == 201:
            self.user_id = user_res.get_json()["id"]
        elif user_res.status_code == 400:
            user = facade.get_user_by_email("test.user@example.com")
            self.user_id = user.id
        else:
            self.fail(f"Unexpected status code creating test user: {user_res.status_code}")

    def test_update_user_valid(self):
        post_res = self.client.post('/api/v1/users/', json={
            "first_name": "Anna",
            "last_name": "Dupont",
            "email": f"anna-{uuid.uuid4()}@example.com",
            "password": "pass"
        }, headers=self.headers)
        self.assertEqual(post_res.status_code, 201)
        user_id = post_res.get_json()["id"]

        put_res = self.client.put(f'/api/v1/users/{user_id}', json={
            "first_name": "Anna-Marie",
            "last_name": "Dupont",
            "email": f"anna-marie-{uuid.uuid4()}@example.com",
            "password": "newpass"
        }, headers=self.headers)
        self.assertEqual(put_res.status_code, 200)
        self.assertEqual(put_res.get_json()["first_name"], "Anna-Marie")

if __name__ == '__main__':
    unittest.main()
