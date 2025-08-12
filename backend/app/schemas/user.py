from pydantic import BaseModel
from typing import Optional

class UserBase(BaseModel):
    username: str
    is_admin: bool = False

class UserCreate(BaseModel):
    username: str
    password: str
    is_admin: Optional[bool] = False

class UserRead(BaseModel):
    id: int
    username: str
    is_admin: bool

class UserUpdate(BaseModel):
    username: Optional[str] = None
    password: Optional[str] = None
    is_admin: Optional[bool] = None

class UserRead(UserBase):
    id: int

    class Config:
        orm_mode = True
