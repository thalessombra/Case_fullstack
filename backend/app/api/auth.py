from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.future import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import timedelta
from app.db.base import get_db as get_async_session
from app.db.models import User
from app.core.security import verify_password, hash_password, create_access_token
from app.core.config import settings
from app.schemas.auth import Token, UserCreate
from app.db.models import Client

router = APIRouter()

@router.post("/token")
async def login_for_access_token(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: AsyncSession = Depends(get_async_session)
):
    
    result = await db.execute(select(Client).filter(Client.email == form_data.username))
    client = result.scalar_one_or_none()
    if not client:
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    if not verify_password(form_data.password, client.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    
    access_token_expires = timedelta(minutes=480)  
    access_token = create_access_token(
        data={"sub": client.email}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}
@router.post("/users", response_model=dict)
async def create_user(user_in: UserCreate, db: AsyncSession = Depends(get_async_session)):
    result = await db.execute(select(User).filter(User.username == user_in.username))
    existing_user = result.scalar_one_or_none()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already registered")
    user = User(
        username=user_in.username,
        hashed_password=hash_password(user_in.password),
        is_admin=user_in.is_admin,
    )
    db.add(user)
    await db.commit()
    await db.refresh(user)
    return {"username": user.username, "is_admin": user.is_admin}
