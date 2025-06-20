# HBnB Project - Part 2: Business Logic and API Endpoints

## Overview

This part of the HBnB project focuses on implementing the core functionality of a RESTful web service for managing users, places, reviews, and amenities. It builds upon the system design created in Part 1 and lays the groundwork for future enhancements such as JWT authentication and database persistence (to be handled in Part 3).

The application is developed using **Python**, **Flask**, and **Flask-RESTx**, structured into modular layers: Presentation, Business Logic, and a temporary in-memory Persistence layer.

## Project Goals

- Structure the application using clean architecture principles  
- Implement core business entities and their relationships  
- Expose a RESTful API for CRUD operations on all entities (except DELETE for User, Place, and Amenity)  
- Implement validation at the business logic layer  
- Perform testing via cURL and unit tests  

---

## Directory Structure

```
hbnb/
├── app/
│   ├── api/
│   ├── __init__.py
│   ├── models/
│   ├── persistence/
│   ├── __pycache__/
│   └── services/
├── config.py
├── run.py
├── README.md
├── requirements.txt
├── tests/
│   ├── __init__.py
│   ├── README.md
│   ├── test_user.py
│   ├── test_place.py
│   ├── test_review.py
│   └── test_amenity.py
└── venv/
```

---

## Implemented Endpoints

| Resource  | Endpoint             | Methods Supported              |
| --------- | -------------------- | ------------------------------ |
| Users     | `/api/v1/users/`     | `POST`, `GET`, `PUT`           |
| Places    | `/api/v1/places/`    | `POST`, `GET`, `PUT`           |
| Reviews   | `/api/v1/reviews/`   | `POST`, `GET`, `PUT`, `DELETE` |
| Amenities | `/api/v1/amenities/` | `POST`, `GET`, `PUT`           |

> Swagger UI: `http://127.0.0.1:5000/api/v1/`

---

## Business Logic Summary

- Validation is handled at the model level before data persistence.
- Place entity checks latitude, longitude ranges, and positive price.
- User creation ensures valid email formats and non-empty names.
- Reviews validate presence of `user_id` and `place_id`.

---

## Validation Rules

### User
- `first_name`, `last_name`, `email`: must not be empty
- `email`: must follow valid format

### Place
- `title`: required
- `price`: positive float
- `latitude`: -90 to 90
- `longitude`: -180 to 180

### Review
- `text`: non-empty
- `user_id`, `place_id`: must reference existing entities

---

## Testing Summary

### ✅ Manual Tests (cURL)
- All endpoints tested using cURL
- Edge cases tested (e.g., missing fields, invalid formats)
- Results documented in `task_06_test.md`

### ✅ Unit Tests (unittest)
Unit tests are located in the `tests/` directory. Example:

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

    def test_create_user_invalid(self):
        response = self.client.post('/api/v1/users/', json={
            "first_name": "",
            "last_name": "",
            "email": "bad-email"
        })
        self.assertEqual(response.status_code, 400)
```

---

## Authors

This project was developed as part of the Holberton School curriculum by Simon(80%) and Ryota(20%)

---

## License

MIT License (2025)


