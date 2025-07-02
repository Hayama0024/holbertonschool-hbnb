from app.models import BaseModel

class Amenity(BaseModel):
    
    def __init__(self, name):
        """
        Amenity class.
        """
        super().__init__()
		
		if not name or not isinstance(name, str) or len(name.strip()) == 0:
            raise ValueError("Invalid name")
        
		self.name = name

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name
        }
