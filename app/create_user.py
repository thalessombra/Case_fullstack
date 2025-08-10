import asyncio
from sqlalchemy import text
from app.db.base import AsyncSessionLocal  # seu sessionmaker
from app.db.models import User
from app.core.security import hash_password

async def create_admin_user(username: str, password: str):
    async with AsyncSessionLocal() as session:
        async with session.begin():
            result = await session.execute(
                text("SELECT * FROM users WHERE username = :username"),
                {"username": username}
            )
            existing_user = result.first()
            if existing_user:
                print("Usuário já existe!")
                return
            
            hashed_pwd = hash_password(password)
            new_user = User(
                username=username,
                hashed_password=hashed_pwd,
                is_admin=True
            )
            session.add(new_user)
        await session.commit()
    print("Usuário admin criado com sucesso!")

if __name__ == "__main__":
    username = "adminmaster"
    password = "supersegura123"
    asyncio.run(create_admin_user(username, password))
