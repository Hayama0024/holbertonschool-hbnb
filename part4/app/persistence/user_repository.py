from app.models.user import User
from app import db
from app.persistence.repository import SQLAlchemyRepository

class UserRepository(SQLAlchemyRepository):
    def __init__(self):
        super().__init__(User)

    def get_user_by_email(self, email):
        return self.model.query.filter_by(email=email).first()

    def create(self, data):
        # Pass the `hashed` flag from input data, default to False
        user = User(
            first_name=data.get('first_name'),
            last_name=data.get('last_name'),
            email=data.get('email'),
            password=data.get('password'),
            hashed=data.get('hashed', False)  # ← FIXED HERE
        )
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user, **kwargs):
        if 'password' in kwargs:
            user.hash_password(kwargs.pop('password'))
        for key, value in kwargs.items():
            if hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user
