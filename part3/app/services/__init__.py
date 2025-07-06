from app.services.facade import HBnBFacade
from app.persistence.repository import InMemoryRepository

facade = HBnBFacade(
    user_repository=InMemoryRepository()
)
