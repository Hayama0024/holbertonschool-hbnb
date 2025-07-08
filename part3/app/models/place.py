# app/models/place.py

from app import db
from app.models.base_model import BaseModel

class Place(BaseModel):
    __tablename__ = 'places'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    price_per_night = db.Column(db.Float, nullable=True)
    max_guests = db.Column(db.Integer, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "address": self.address,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
