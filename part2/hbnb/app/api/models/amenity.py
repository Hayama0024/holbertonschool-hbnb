from app.models.base_model import BaseModel


class Amenity(BaseModel):
    def __init__(self, name: str):
        super().__init__()
        if not isinstance(name, str) or len(name) > 50:
            raise ValueError("Name must be a string of max 50 characteres")

        self.name: str = name
