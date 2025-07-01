from app.models.base_model import BaseModel
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(BaseModel):
    __tablename__ = "users"

    # The user's email address (must be unique and not null)
    email = db.Column(db.String(128), unique=True, nullable=False)

    # The hashed password (not stored in plain text)
    password_hash = db.Column(db.String(128), nullable=False)

    @property
    def password(self):
        """Prevent direct access to the password."""
        raise AttributeError("Password is not readable.")

    @password.setter
    def password(self, password):
        """Hash the password and store it securely."""
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        """Verify the password against the stored hash."""
        return check_password_hash(self.password_hash, password)
