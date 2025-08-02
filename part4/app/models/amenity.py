from app.models import BaseModel
from app import db

# ✅ Place と Amenity の中間テーブル（ID 型は String(36) で統一）
place_amenities = db.Table(
    'place_amenities',
    db.Column('place_id', db.String(36), db.ForeignKey('places.id'), primary_key=True),
    db.Column('amenity_id', db.String(36), db.ForeignKey('amenities.id'), primary_key=True),
)

class Amenity(BaseModel):
    __tablename__ = 'amenities'

    name = db.Column(db.String(128), nullable=False, unique=True)

    def __init__(self, name):
        super().__init__()

        if not name or len(name) > 128:
            raise ValueError("Invalid name")

        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "created_at": self.created_at.isoformat() if self.created_at else None,
            "updated_at": self.updated_at.isoformat() if self.updated_at else None
        }
