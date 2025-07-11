from app import db
import uuid
from datetime import datetime

class BaseModel(db.Model):
    """
    Abstract base
    """
    __abstract__ = True

    id = db.Column(db.String(36), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def save(self):
        """
        Commit this object to the database.
        """
        db.session.add(self)
        db.session.commit()

    def update(self, data):
        """
        Updates existing attributes and commits.
        """
        for key, value in data.items():
            if hasattr(self, key):
                setattr(self, key, value)
        self.updated_at = datetime.utcnow()
        self.save()

    def to_dict(self):
        """
        Returns a dict representation
        """
        return {c.name: getattr(self, c.name) for c in self.__table__.columns}
