# Task 6: Endpoint Testing and Validation Report

## ✅ Endpoint: `POST /api/v1/users/`

### Success Case
- **Input**:
  ```json
  {
    "first_name": "Alice",
    "last_name": "Wonderland",
    "email": "alice@example.com"
  }
  ```
- **Expected Status**: 201 Created  
- **Actual Result**: ✅ Success

### Failure Case: Duplicate Email
- **Input**:
  ```json
  {
    "first_name": "John",
    "last_name": "Doe",
    "email": "john.doe@example.com"
  }
  ```
- **Expected Status**: 400 Bad Request  
- **Actual Result**: ❌ "Email already registered"

### Failure Case: Invalid Input
- **Input**:
  ```json
  {
    "first_name": "",
    "last_name": "",
    "email": "not-an-email"
  }
  ```
- **Expected Status**: 400 Bad Request  
- **Actual Result**: ❌ "Invalid input data"

---

## ✅ Endpoint: `POST /api/v1/places/`

### Success Case
- **Input**:
  ```json
  {
    "title": "Cozy Cabin",
    "description": "A nice quiet place in the woods",
    "price": 80.0,
    "latitude": 45.0,
    "longitude": 2.0,
    "owner_id": "f992f153-4da2-4d9a-aa82-85a89c70d320"
  }
  ```
- **Expected Status**: 201 Created  
- **Actual Result**: ✅ Success

### Failure Case: Latitude Out of Range
- **Input**:
  ```json
  {
    "title": "Too Far North",
    "price": 50,
    "latitude": 100,
    "longitude": 10,
    "owner_id": "f992f153-4da2-4d9a-aa82-85a89c70d320"
  }
  ```
- **Expected**: 400  
- **Actual**: ❌ "Latitude must be between -90 and 90."

### Failure Case: Empty Title
- **Input**:
  ```json
  {
    "title": "",
    "price": 50,
    "latitude": 45,
    "longitude": 10,
    "owner_id": "f992f153-4da2-4d9a-aa82-85a89c70d320"
  }
  ```
- **Expected**: 400  
- **Actual**: ❌ "Invalid title"

### Failure Case: Negative Price
- **Input**:
  ```json
  {
    "title": "Negative Price House",
    "price": -10,
    "latitude": 45,
    "longitude": 10,
    "owner_id": "f992f153-4da2-4d9a-aa82-85a89c70d320"
  }
  ```
- **Expected**: 400  
- **Actual**: ❌ "Price must be a non-negative float."

---

## 🧪 Unit Testing (`tests/test_user.py`)

```python
import unittest
from app import create_app

class TestUserEndpoints(unittest.TestCase):

    def setUp(self):
        self.app = create_app()
        self.client = self.app.test_client()

    def test_create_user(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "Jane",
            "last_name": "Doe",
            "email": "jane.doe@example.com"
        })
        self.assertEqual(response.status_code, 201)

    def test_create_user_invalid_data(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "invalid-email"
        })
        self.assertEqual(response.status_code, 400)
```

---

## Notes
- ✅ Swagger UI available at: `http://127.0.0.1:5000/api/v1/`
- ✅ Validation implemented in the business logic layer
- 🟡 Manual cURL testing completed for `User` and `Place`
- 🔜 Testing for `Review` and `Amenity` planned next
