from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository, AmenityRepository

facade = HBnBFacade(
    user_repository=InMemoryRepository(),
    place_repository=InMemoryRepository(),
    review_repository=InMemoryRepository(),
    amenity_repository=AmenityRepository()
)
