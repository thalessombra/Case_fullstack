from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.models import User
from app.schemas.user import UserCreate, UserRead, UserUpdate
from app.db.base import get_db as get_async_session
from app.core.security import hash_password
from app.core.deps import get_current_user, require_admin

router = APIRouter()

@router.post("/users", response_model=UserRead, status_code=status.HTTP_201_CREATED)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    
    result = await db.execute(select(User).filter(User.username == user_in.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        is_admin=getattr(user_in, "is_admin", False) or False,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user



@router.get("/users", response_model=List[UserRead])
async def read_users(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, alias="search"),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    query = select(User)
    if search:
        query = query.filter(User.username.ilike(f"%{search}%"))
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    users = result.scalars().all()
    return users


@router.get("/users{user_id}", response_model=UserRead)
async def read_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return user


@router.put("/users{user_id}", response_model=UserRead)
async def update_user(
    user_id: int,
    user_in: UserUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if user_in.username is not None:
        # Verifica se username já existe para outro usuário
        result = await db.execute(
            select(User).filter(User.username == user_in.username, User.id != user_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Username already registered by another user")
        user.username = user_in.username
    if user_in.password is not None:
        user.hashed_password = hash_password(user_in.password)
    if user_in.is_admin is not None:
        user.is_admin = user_in.is_admin

    db.add(user)
    await db.commit()
    await db.refresh(user)
    return user


@router.delete("/users{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(User).filter(User.id == user_id))
    user = result.scalar_one_or_none()
    if user is None:
        raise HTTPException(status_code=404, detail="User not found")

    await db.delete(user)
    await db.commit()
    return None
