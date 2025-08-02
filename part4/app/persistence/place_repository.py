from app import db
from app.models.place import Place
from app.persistence.repository import SQLAlchemyRepository

class PlaceRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(Place)

    def get_by_title(self, title):

        return self.model.query.filter_by(title=title).first()
