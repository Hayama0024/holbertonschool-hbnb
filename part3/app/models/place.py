# app/models/place.py

from app import db
from app.models.base_model import BaseModel

place_amenity = db.Table('place_amenity',
    db.Column('place_id', db.String(60), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(60), db.ForeignKey('amenities.id'), primary_key=True)
)

class Place(BaseModel):
    __tablename__ = 'places'

    name = db.Column(db.String(128), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    city = db.Column(db.String(128), nullable=True)
    address = db.Column(db.String(256), nullable=True)
    price_per_night = db.Column(db.Float, nullable=True)
    max_guests = db.Column(db.Integer, nullable=True)

    user_id = db.Column(db.String(60), db.ForeignKey('users.id'), nullable=False)
    reviews = db.relationship('Review', backref='place', lazy=True)
    amenities = db.relationship('Amenity', secondary=place_amenity, backref=db.backref('places', lazy=True), lazy='subquery')


    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "description": self.description,
            "city": self.city,
            "address": self.address,
            "price_per_night": self.price_per_night,
            "max_guests": self.max_guests,
            "user_id": self.user_id,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
