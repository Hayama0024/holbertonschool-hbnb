# main.py

from app import db
from app import create_app
from app.config import DevelopmentConfig
from app.models import User

app = create_app(DevelopmentConfig)

with app.app_context():
    db.create_all()
    print("User table created successfully!")
