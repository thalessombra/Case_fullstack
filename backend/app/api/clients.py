from fastapi import APIRouter, Depends, HTTPException, Query, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select
from typing import List, Optional

from app.db.models import Client
from app.schemas.client import ClientCreate, ClientRead, ClientUpdate
from app.db.base import get_db as get_async_session
from app.core.security import hash_password
from app.core.deps import get_current_user, require_admin

router = APIRouter()

@router.post("/clients/", response_model=ClientRead)
async def create_client(
    client_in: ClientCreate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Client).filter(Client.email == client_in.email))
    existing = result.scalar_one_or_none()
    if existing:
        raise HTTPException(status_code=400, detail="Email already registered")

    client = Client(
        name=client_in.name,
        email=client_in.email,
        hashed_password=hash_password(client_in.password),
        is_active=client_in.is_active,
        role=client_in.role if hasattr(client_in, 'role') else "read-only",
    )
    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

@router.get("/clients/", response_model=List[ClientRead])
async def read_clients(
    skip: int = 0,
    limit: int = 10,
    search: Optional[str] = Query(None, alias="search"),
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    query = select(Client)
    if search:
        query = query.filter(
            (Client.name.ilike(f"%{search}%")) | (Client.email.ilike(f"%{search}%"))
        )
    query = query.offset(skip).limit(limit)
    result = await db.execute(query)
    clients = result.scalars().all()
    return clients

@router.get("/clients/{client_id}", response_model=ClientRead)
async def read_client(
    client_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(get_current_user),
):
    result = await db.execute(select(Client).filter(Client.id == client_id))
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")
    return client

@router.put("/clients/{client_id}", response_model=ClientRead)
async def update_client(
    client_id: int,
    client_in: ClientUpdate,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Client).filter(Client.id == client_id))
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    if client_in.name is not None:
        client.name = client_in.name
    if client_in.email is not None:
        result = await db.execute(
            select(Client).filter(Client.email == client_in.email, Client.id != client_id)
        )
        existing = result.scalar_one_or_none()
        if existing:
            raise HTTPException(status_code=400, detail="Email already registered by another client")
        client.email = client_in.email
    if client_in.is_active is not None:
        client.is_active = client_in.is_active
    if hasattr(client_in, "role") and client_in.role is not None:
        client.role = client_in.role

    db.add(client)
    await db.commit()
    await db.refresh(client)
    return client

@router.delete("/clients/{client_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_client(
    client_id: int,
    db: AsyncSession = Depends(get_async_session),
    current_user=Depends(require_admin),
):
    result = await db.execute(select(Client).filter(Client.id == client_id))
    client = result.scalar_one_or_none()
    if client is None:
        raise HTTPException(status_code=404, detail="Client not found")

    await db.delete(client)
    await db.commit()
    return None
