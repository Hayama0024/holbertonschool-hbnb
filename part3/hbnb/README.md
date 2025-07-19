HBnB Project - Part 3: Enhanced Backend with Authentication and Database Integration

Overview

This project is Part 3 of the Holberton School HBnB series. It focuses on securing and scaling the backend with persistent database storage, JWT-based authentication, and role-based access control. The project uses Flask, SQLAlchemy, and Flask-JWT-Extended to create a real-world backend API resembling Airbnb functionality.

Features

・JWT authentication and session management
・ Role-based access control (is admin)
・ RESTful CRUD API for:
Users
Places
Reviews
Amenities
・ SQLite for development, MySQL-ready for production
・ Password hashing with bcrypt
・ ER diagram with Mermaid.js
・ Validations across models and service layer
・ Modular design with repository and facade patterns

Tech Stack

Python 3
Flask
Flask-RESTx
Flask-JWT-Extended
Flask-Bcrypt
SQLAlchemy
SQLite / MySQL
Mermaid.js
Pytest / Unittest

⚙️ Setup Instructions
# 1. Clone the repository
git clone https://github.com/YOUR_USERNAME/holbertonschool-hbnb.git -b simon part3
cd part3

# 2. Create and activate virtual environment
python3 -m venv venv
source venv/bin/activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set environment variables (for dev)
export FLASK_APP=run.py
export FLASK_ENV=development
export JWT_SECRET_KEY="your_secret_key"

# 5. Run migrations (if using Flask-Migrate)
flask db init
flask db migrate
flask db upgrade

# 6. Start the Flask app
flask run


Project Structure
part3/
└── hbnb
    ├── app/
    │   ├── api/v1/                # API namespaces
    │   ├── models/                # SQLAlchemy models
    │   ├── persistence/           # Repositories
    │   └── services/              # Facade (service logic)
    ├── config.py                  # Configuration class
    ├── run.py                     # App bootstrap
    └── tests/                     # Unittest test files

🔐 Authentication Flow

Register: POST /api/v1/users/
Login: POST /api/v1/auth/login → Returns JWT
Protected Routes: Require Authorization: Bearer <token> header
Admin-only Routes: Require JWT with is_admin=true claim


Entity-Relationship Diagram

User owns many Place
User writes many Review
Place receives many Review
Place includes many Amenity via Place_Amenity (M2M)

![ER Diagram](./Database%20diagram.png)


🧬 Data Models Summary

User
Field	Type	Notes
id	UUID	Primary Key
first_name	string	Required, max 50 chars
last_name	string	Required, max 50 chars
email	string	Unique, validated
password	string	Hashed using bcrypt
is_admin	bool	Admin role flag

Place
Field	Type	Notes
title	string	Required, max 100 chars
description	string	Optional
price	float	Required, ≥ 0
latitude	float	Between -90 and 90
longitude	float	Between -180 and 180
owner_id	UUID	FK → User

Review
Field	Type	Notes
text	string	Required
rating	int	1 to 5
user_id	UUID	FK → User
place_id	UUID	FK → Place
Amenity
Field	Type	Notes
name	string	Unique, max 128 chars


🔐 Role-Based Access Control

Action	Auth Required	Admin Only
Register User	❌	❌
Login	❌	❌
View Places / Reviews / Amenities	❌	❌
Create Place / Review	✅	❌
Modify Own Place / Review	✅	❌
Create/Update Any User or Amenity	✅	✅
View All Users	✅	✅


 Testing
 # Run all unit tests
 python3 -m unittest discover hbnb/tests

Tests are written using unittest, covering:
・User creation and hashing
・JWT authentication
・CRUD operations on Places, Reviews, Amenities
・Admin access logic

Author
Simon Paulin


License

This project is licensed for educational purposes under Holberton School curriculum.


