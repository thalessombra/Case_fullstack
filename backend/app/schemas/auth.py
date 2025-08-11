from pydantic import BaseModel, EmailStr

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class TokenData(BaseModel):
    email: EmailStr | None = None
    role: str | None = None

class UserCreate(BaseModel):
    email: EmailStr
    password: str
    role: str  # "admin" ou "read-only"
