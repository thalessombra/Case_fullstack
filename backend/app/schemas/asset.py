# app/schemas/asset.py
from pydantic import BaseModel
from typing import Optional

class AssetBase(BaseModel):
    ticker: str
    name: Optional[str] = None

class AssetCreate(AssetBase):
    pass

class AssetUpdate(BaseModel):
    ticker: Optional[str] = None
    name: Optional[str] = None

class AssetRead(AssetBase):
    id: int

    class Config:
        orm_mode = True
