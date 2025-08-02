import re
from app import db, bcrypt
from app.models import BaseModel

class User(BaseModel):
    __tablename__ = 'users'

    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=True)
    is_admin = db.Column(db.Boolean, default=False)

    def __init__(self, first_name, last_name, email, password=None, hashed=False):
        super().__init__()

        if not first_name or len(first_name) > 50:
            raise ValueError("Invalid first_name")
        if not last_name or len(last_name) > 50:
            raise ValueError("Invalid last_name")
        if not email or not self._is_valid_email(email):
            raise ValueError("Invalid email")

        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.is_admin = False

        if password:
            if hashed:
                self.password = password
            else:
                self.hash_password(password)
        else:
            self.password = None

    def _is_valid_email(self, email):
        regex = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        return re.match(regex, email) is not None

    def to_dict(self):
        return {
            'id': self.id,
            'first_name': self.first_name,
            'last_name': self.last_name,
            'email': self.email,
        }

    def hash_password(self, password):
        self.password = bcrypt.generate_password_hash(password).decode('utf-8')

    def verify_password(self, password):
        return bcrypt.check_password_hash(self.password, password)
