import uuid
from datetime import datetime

class BaseModel:
    """
    Initializes a unique identifier.
    """
    def __init__(self):
        self.id = str(uuid.uuid4())
        self.created_at = datetime.now()
        self.updated_at = datetime.now()

    def save(self):
        """
        Updates attribute with the current time.
        """
        self.updated_at = datetime.now()

    def update(self, data):
        """
        Updates existing attributes.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.save()

    def to_dict(self):
        result = self.__dict__.copy()
        return result
    