from pydantic import BaseModel, EmailStr


class ClientBase(BaseModel):
    name: str
    email: EmailStr
    is_active: bool = True


class ClientCreate(ClientBase):
    password: str  


class ClientRead(ClientBase):
    id: int

    class Config:
        orm_mode = True


class ClientUpdate(BaseModel):
    name: str | None = None
    email: EmailStr | None = None
    password: str | None = None
    is_active: bool | None = None
