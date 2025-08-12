from pydantic import BaseModel
from datetime import date
from typing import Optional

class AllocationBase(BaseModel):
    client_id: int
    asset_id: int
    qty: float
    price: float
    bought_at: date

class AllocationCreate(AllocationBase):
    pass

class AllocationUpdate(BaseModel):
    qty: Optional[float] = None
    price: Optional[float] = None
    bought_at: Optional[date] = None

class AllocationRead(AllocationBase):
    id: int

    class Config:
        orm_mode = True
