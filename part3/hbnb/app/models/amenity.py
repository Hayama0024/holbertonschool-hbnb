from app.models import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        """
        Amenity class.
        """
        super().__init__()
        self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
