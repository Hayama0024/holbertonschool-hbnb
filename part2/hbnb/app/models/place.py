from app.models import BaseModel

class Place(BaseModel):
    def __init__(self, title, price, latitude, longitude, owner, description=""):
        """
        Place class, which inherits from BaseModel.
        """
        super().__init__()

        if not title or len(title) > 100:
            raise ValueError("Invalid title")
        if price < 0:
            raise ValueError("Price must be positive")
        if not (-90.0 <= latitude <= 90.0):
            raise ValueError("Latitude out of range")
        if not (-180.0 <= longitude <= 180.0):
            raise ValueError("Longitude out of range")
        if not hasattr(owner, 'id'):
            raise ValueError("Invalid owner")

        self.title = title
        self.description = description
        self.price = price
        self.latitude = latitude
        self.longitude = longitude
        self.owner = owner
        self.reviews = []
        self.amenities = []

    def add_review(self, review):
        self.reviews.append(review)

    def add_amenity(self, amenity):
        self.amenities.append(amenity)

    def to_dict(self):
        return {
            'id': self.id,
            'title': self.title,
            'description': self.description,
            'price': self.price,
            'latitude': self.latitude,
            'longitude': self.longitude,
            'owner_id': self.owner.id if hasattr(self.owner, 'id') else None,
            'amenities': [a.id for a in self.amenities],
            'created_at': self.created_at.isoformat() if hasattr(self, 'created_at') else None,
        }
