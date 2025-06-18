from base_model import BaseModel


class User(BaseModel):
    def __init__(
        self,
        first_name: str,
        last_name: str,
        email: str,
        is_admin: bool = False
    ):
        super().__init__()
        if not isinstance(first_name, str) or len(first_name) > 50:
            raise ValueError(
                "First name must be a string of maximum of 50 characters."
            )
        if not isinstance(last_name, str) or len(last_name) > 50:
            raise ValueError(
                "Last name must be a string of maximum of 50 characters."
            )
        if not isinstance(email, str) or "@" not in email:
            raise ValueError("Valide email required")
        if not isinstance(is_admin, bool):
            raise ValueError("is_admin must be a Boolean")

        self.first_name: str = first_name
        self.last_name: str = last_name
        self.email: str = email
        self.is_admin: bool = is_admin
