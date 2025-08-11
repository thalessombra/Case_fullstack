from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta

from app.db.base import get_db as get_async_session
from app.core.security import verify_password, hash_password, create_access_token
from app.schemas.auth import Token, UserCreate
from app.db.models import User  # usar User

router = APIRouter()

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session),
):
    result = await db.execute(select(User).filter(User.username == form_data.username))
    user = result.scalar_one_or_none()
    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=480)
    access_token = create_access_token(
        data={"sub": user.username, "is_admin": user.is_admin}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.post("/users", response_model=dict)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.username == user_in.email.split("@")[0]))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")

    user = User(
        username=user_in.email.split("@")[0],  # username gerado pelo email antes do @
        hashed_password=hash_password(user_in.password),
        is_admin=user_in.role.lower() == "admin",
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"username": user.username, "is_admin": user.is_admin}
