# app/models/base_model.py

from datetime import datetime
from app import db
import uuid

class BaseModel(db.Model):
    __abstract__ = True

    id = db.Column(db.String(60), primary_key=True, default=lambda: str(uuid.uuid4()))
    created_at = db.Column(db.DateTime, default=datetime.utcnow)
    updated_at = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

