from app.models.base_model import BaseModel
from app.models.user import User


class Place(BaseModel):
    def __init__(
        self,
        title: str,
        description: str,
        price: float,
        latitude: float,
        longitude: float,
        owner: User
    ):
        super().__init__()
        if not isinstance(title, str) or len(title) > 100:
            raise ValueError(
                "Title must be a string of maximum of 100 charateres."
            )
        if description is not None and not isinstance(description, str):
            raise ValueError("Description must be a string")

        if not isinstance(price, (float, int)) or price < 0:
            raise ValueError("Price must be a positive float.")

        if not isinstance(latitude, (float, int)) or not -90 <= latitude <= 90:
            raise ValueError("Latitude must be between -90 and 90.")

        if (
            not isinstance(longitude, (float, int))
            or not -180 <= longitude <= 180
        ):
            raise ValueError("Longitude must be between -180 and 180.")
        if not isinstance(owner, User):
            raise ValueError("Owner must be a User instance")

        self.title: str = title
        self.description: str = description
        self.price: float = price
        self.latitude: float = latitude
        self.longitude: float = longitude
        self.owner: User = owner
        self.reviews: list = []  # List to store related reviews
        self.amenities: list = []  # List to store related amenities

    def add_review(self, review):
        """Add a review to the place."""
        self.reviews.append(review)

    def add_amenity(self, amenity):
        """Add an amenity to the place."""
        self.amenities.append(amenity)