import pytest
from app import create_app
import json

@pytest.fixture
def client():
    app = create_app()
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_create_user(client):
    response = client.post(
        '/api/v1/users/',
        data=json.dumps({
            "first_name": "Test",
            "last_name": "User",
            "email": "testuser@test.com",
            "password": "Secret1234"
        }),
        content_type='application/json'
    )
    assert response.status_code == 201
    data = response.get_json()
    assert 'id' in data
    assert 'message' in data
    assert 'password' not in data

def test_get_users(client):
    response = client.get('/api/v1/users/')
    assert response.status_code == 200
    users = response.get_json()
    for user in users:
        assert 'password' not in user

def test_get_user_detail(client):
    post_resp = client.post(
        '/api/v1/users/',
        data=json.dumps({
            "first_name": "Detail",
            "last_name": "Tester",
            "email": "detailtester@test.com",
            "password": "SuperSecret"
        }),
        content_type='application/json'
    )
    user_id = post_resp.get_json()['id']

    get_resp = client.get(f'/api/v1/users/{user_id}')
    assert get_resp.status_code == 200
    user = get_resp.get_json()
    assert 'password' not in user
    assert user['email'] == "detailtester@test.com"
