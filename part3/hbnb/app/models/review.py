from app.models import BaseModel
from app import db
from sqlalchemy.orm import relationship

class Review(BaseModel):
    __tablename__ = 'reviews'

    text = db.Column(db.String(1024), nullable=False)
    rating = db.Column(db.Integer, nullable=False)

    user_id = db.Column(db.String(36), db.ForeignKey('users.id'), nullable=False)
    place_id = db.Column(db.String(36), db.ForeignKey('places.id'), nullable=False)

    user = relationship('User', backref='reviews')
    place = relationship('Place', backref='reviews')

    def __init__(self, text, rating, place, user):
        super().__init__()

        if not text:
            raise ValueError("Review text is required")
        if not (1 <= rating <= 5):
            raise ValueError("Rating must be between 1 and 5")
        if not isinstance(place, object) or not hasattr(place, 'id'):
            raise ValueError("Invalid place")
        if not isinstance(user, object) or not hasattr(user, 'id'):
            raise ValueError("Invalid user")

        self.text = text
        self.rating = rating
        self.place = place
        self.user = user

    def to_dict(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
            'user_id': self.user.id if self.user else None,
            'place_id': self.place.id if self.place else None,
            'created_at': self.created_at.isoformat() if self.created_at else None,
            'updated_at': self.updated_at.isoformat() if self.updated_at else None,
        }

    def to_dict_get(self):
        return {
            'id': self.id,
            'text': self.text,
            'rating': self.rating,
        }
