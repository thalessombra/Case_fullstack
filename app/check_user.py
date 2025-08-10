import asyncio
import asyncpg

async def main():
    conn = await asyncpg.connect(
    user='invest',
    password='investpw',
    database='investdb',
    host='db',      # nome do serviço do banco no docker-compose
    port=5432       # porta interna padrão do PostgreSQL no container
)

    # Verifica se a coluna hashed_password existe na tabela clients
    col_info = await conn.fetch(
        """
        SELECT column_name 
        FROM information_schema.columns 
        WHERE table_name='clients' AND column_name='hashed_password';
        """
    )
    if col_info:
        print("Coluna 'hashed_password' existe na tabela clients.")
    else:
        print("Coluna 'hashed_password' NÃO existe na tabela clients.")

    # Busca dados do usuário adminmaster
    user = await conn.fetchrow(
        "SELECT id, email, hashed_password FROM clients WHERE email = 'adminmaster';"
    )
    if user:
        print(f"Usuário encontrado: id={user['id']}, email={user['email']}, hashed_password={user['hashed_password']}")
    else:
        print("Usuário 'adminmaster' NÃO encontrado.")


    await conn.close()

if __name__ == "__main__":
    asyncio.run(main())
