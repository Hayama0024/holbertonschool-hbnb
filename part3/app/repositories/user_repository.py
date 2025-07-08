from app.models.user import User
from app import db
from typing import Optional, List


class UserRepository:
    def get_all(self) -> List[User]:
        return User.query.all()

    def get_by_id(self, user_id: str) -> Optional[User]:
        return User.query.get(user_id)

    def get_by_email(self, email: str) -> Optional[User]:
        return User.query.filter_by(email=email).first()

    def create(self, data: dict) -> User:
        user = User(**data)
        db.session.add(user)
        db.session.commit()
        return user

    def update(self, user: User, **kwargs) -> User:
        for key, value in kwargs.items():
            if key == 'password':
                user.set_password(value)
            elif hasattr(user, key):
                setattr(user, key, value)
        db.session.commit()
        return user

    def delete(self, user_id: str) -> bool:
        user = self.get_by_id(user_id)
        if not user:
            return False
        db.session.delete(user)
        db.session.commit()
        return True

