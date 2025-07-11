from app.models import BaseModel
from app import db

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
