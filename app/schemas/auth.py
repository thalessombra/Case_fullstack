from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    username: str | None = None
    is_admin: bool = False

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: bool = False
