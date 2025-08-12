
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.models import Asset
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.db.base import get_db as get_async_session
from app.core.deps import get_current_user, require_admin

router = APIRouter()


@router.post("/", response_model=AssetRead, status_code=status.HTTP_201_CREATED)
async def create_asset(
    asset_in: AssetCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),  # apenas admin pode criar assets
):
    # evita duplicidade pelo ticker
    result = await db.execute(select(Asset).filter(Asset.ticker == asset_in.ticker))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Asset with this ticker already exists")

    asset = Asset(ticker=asset_in.ticker.upper(), name=asset_in.name)
    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.get("/", response_model=List[AssetRead])
async def read_assets(
    skip: int = 0,
    limit: int = 100,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    q = select(Asset).offset(skip).limit(limit)
    result = await db.execute(q)
    assets = result.scalars().all()
    return assets


@router.get("/{asset_id}", response_model=AssetRead)
async def read_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Asset).filter(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")
    return asset


@router.put("/{asset_id}", response_model=AssetRead)
async def update_asset(
    asset_id: int,
    asset_in: AssetUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Asset).filter(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    if asset_in.ticker is not None:
        asset.ticker = asset_in.ticker.upper()
    if asset_in.name is not None:
        asset.name = asset_in.name

    db.add(asset)
    await db.commit()
    await db.refresh(asset)
    return asset


@router.delete("/{asset_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_asset(
    asset_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Asset).filter(Asset.id == asset_id))
    asset = result.scalar_one_or_none()
    if not asset:
        raise HTTPException(status_code=404, detail="Asset not found")

    await db.delete(asset)
    await db.commit()
    return None
