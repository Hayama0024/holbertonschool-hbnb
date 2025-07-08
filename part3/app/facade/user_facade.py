from typing import Optional
from app.models.user import User
from app.repositories.user_repository import UserRepository
from app import bcrypt

class UserFacade:
    def __init__(self):
        self.repository = UserRepository()

    def get_all_users(self):
        return self.repository.get_all()

    def get_user_by_id(self, user_id: str):
        return self.repository.get_by_id(user_id)

    def create_user(self, data: dict):
        password_hash = bcrypt.generate_password_hash(data["password"]).decode('utf-8')
        user_data = data.copy()
        user_data["password"] = password_hash
        return self.repository.create(user_data)
    
    def update_user(self, user_id: str, data: dict) -> Optional[User]:
        user = self.repository.get_by_id(user_id)
        if not user:
            return None
        return self.repository.update(user, **data)

    def delete_user(self, user_id: str):
        return self.repository.delete(user_id)
