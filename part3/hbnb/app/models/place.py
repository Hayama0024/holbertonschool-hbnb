from app.models import BaseModel, place_amenity
from sqlalchemy.orm import relationship
from app import db

class Place(BaseModel):
    __tablename__ = 'places'

    title = db.Column(db.String(100), nullable=False)
    description = db.Column(db.String(512), nullable=True)
    price = db.Column(db.Float, nullable=False)
    latitude = db.Column(db.Float, nullable=False)
    longitude = db.Column(db.Float, nullable=False)
    owner_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    owner = relationship('User', backref='places')

    amenities = db.relationship('Amenity', secondary=place_amenity, backref='places')

    def __init__(self, title, price, latitude, longitude, owner_id, description=""):
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price < 0:
            raise ValueError("Price must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude out of range")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude out of range")

        self.title = title
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner_id = owner_id
        self.description = description

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner_id,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'amenities': [a.to_dict() for a in self.amenities]
        }
