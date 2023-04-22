from pydantic import BaseModel


class User(BaseModel):
    username: str
    password: str | None = None


class VaultUpdate(User):
    vault: str