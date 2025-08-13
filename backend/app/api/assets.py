
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.models import Asset
from app.schemas.asset import AssetCreate, AssetRead, AssetUpdate
from app.db.base import get_db as get_async_session
from app.core.deps import get_current_user, require_admin
import asyncio
from decimal import Decimal
from app.core.redis import get_redis_client
import yfinance as yf

router = APIRouter()

@router.get("/symbol/{symbol}/price", summary="Get price for a ticker with Redis cache")
async def get_asset_price_by_symbol(
    symbol: str,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    """
    Busca preço atual do ticker (ex: AAPL).
    - Primeiro verifica cache Redis (key = price:{SYMBOL}).
    - Se não tiver, busca via yfinance (com retries/back-off) e salva no Redis com TTL 3600s.
    Retorna JSON: { "symbol": "AAPL", "price": 123.45, "source": "cache"|"yfinance" }
    """

    symbol_up = symbol.upper()
    redis = get_redis_client()
    cache_key = f"price:{symbol_up}"

    
    try:
        cached = await redis.get(cache_key)
        if cached is not None:
            
            try:
                price_val = float(cached)
            except Exception:
                price_val = Decimal(cached)
            return {"symbol": symbol_up, "price": float(price_val), "source": "cache"}
    except Exception as e:

        print("Warning: Redis error:", e)

    
    def _sync_fetch_price(sym: str):
        """chamada síncrona feita em executor — usa yfinance internamente"""
        ticker = yf.Ticker(sym)
        hist = ticker.history(period="1d")
        
        if hist is None or hist.empty:
            raise ValueError("No price data for symbol")
        close_price = hist["Close"].iloc[-1]
        return float(close_price)

    
    max_retries = 3
    delay = 1.0
    last_exc = None
    for attempt in range(max_retries):
        try:
            loop = asyncio.get_running_loop()
            price = await loop.run_in_executor(None, _sync_fetch_price, symbol_up)
            
            try:
                await redis.set(cache_key, str(price), ex=3600)
            except Exception as e:
                print("Warning: Redis SET failed:", e)
            return {"symbol": symbol_up, "price": float(price), "source": "yfinance"}
        except Exception as e:
            last_exc = e
            if attempt < max_retries - 1:
                await asyncio.sleep(delay)
                delay *= 2
            else:
                
                raise HTTPException(status_code=502, detail=f"Error fetching price for {symbol_up}: {e}")


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
