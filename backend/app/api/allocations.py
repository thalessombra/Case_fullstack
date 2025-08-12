from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List

from app.db.models import Allocation
from app.schemas.allocation import AllocationCreate, AllocationRead, AllocationUpdate
from app.db.base import get_db as get_async_session
from app.core.deps import get_current_user, require_admin

router = APIRouter()

@router.post("/allocations/", response_model=AllocationRead)
async def create_allocation(
    allocation_in: AllocationCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    allocation = Allocation(**allocation_in.model_dump())
    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    return allocation

@router.get("/allocations/", response_model=List[AllocationRead])
async def read_allocations(
    skip: int = 0,
    limit: int = 10,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    query = select(Allocation).offset(skip).limit(limit)
    result = await db.execute(query)
    allocations = result.scalars().all()
    return allocations

@router.get("/allocations/{allocation_id}", response_model=AllocationRead)
async def read_allocation(
    allocation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Allocation).filter(Allocation.id == allocation_id))
    allocation = result.scalar_one_or_none()
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")
    return allocation

@router.put("/allocations/{allocation_id}", response_model=AllocationRead)
async def update_allocation(
    allocation_id: int,
    allocation_update: AllocationUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin), 
):
    result = await db.execute(select(Allocation).filter(Allocation.id == allocation_id))
    allocation = result.scalar_one_or_none()
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")

    update_data = allocation_update.model_dump(exclude_unset=True)
    for key, value in update_data.items():
        setattr(allocation, key, value)

    db.add(allocation)
    await db.commit()
    await db.refresh(allocation)
    return allocation

@router.delete("/allocations/{allocation_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_allocation(
    allocation_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Allocation).filter(Allocation.id == allocation_id))
    allocation = result.scalar_one_or_none()
    if allocation is None:
        raise HTTPException(status_code=404, detail="Allocation not found")

    await db.delete(allocation)
    await db.commit()
    return None
