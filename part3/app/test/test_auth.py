import pytest
from app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_login_success(client):
    # On crée un utilisateur avant de tester le login
    client.post(
        '/api/v1/users/',
        data=json.dumps({
            "first_name": "Login",
            "last_name": "Tester",
            "email": "loginuser@test.com",
            "password": "PassTestJWT"
        }),
        content_type='application/json'
    )

    # On teste le login
    response = client.post(
        '/api/v1/auth/login',
        data=json.dumps({
            "email": "loginuser@test.com",
            "password": "PassTestJWT"
        }),
        content_type='application/json'
    )
    assert response.status_code == 200
    data = response.get_json()
    assert 'access_token' in data
