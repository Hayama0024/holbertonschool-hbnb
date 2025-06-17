from app.models.base_model import BaseModel
from app.models.user import User
from app.models.place import Place


class Review(BaseModel):
    def __init__(
        self,
        user: User,
        place: Place,
        rating: int,
        text: str
    ):
        super().__init__()
        if not isinstance(user, User):
            raise ValueError("User must be a User instance.")
        if not isinstance(place, Place):
            raise ValueError("Place must be a place instance.")
        if not isinstance(rating, int) or not 1 <= rating <= 5:
            raise ValueError("Rating must be a integer between 1 and 5.")
        if not isinstance(text, str) or not text.strip():
            raise ValueError("Text required and must be a string.")

        self.user: User = user
        self.place: Place = place
        self.rating: int = rating
        self.text: str = text
