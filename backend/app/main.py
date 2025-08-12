from fastapi import FastAPI, Depends, Security
from fastapi.security import OAuth2PasswordBearer, SecurityScopes
from fastapi.openapi.models import OAuth2, OAuthFlows
from fastapi.openapi.utils import get_openapi
from app.db import models
from app.db.base import engine
from fastapi import FastAPI
from app.api import clients, auth, users
from app.api import allocations
from app.api import assets

app = FastAPI(title="Investment API")
app.include_router(clients.router)
app.include_router(auth.router)
app.include_router(allocations.router, prefix="/allocations", tags=["allocations"])
app.include_router(assets.router, prefix="/assets", tags=["assets"])
app.include_router(users.router)
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def custom_openapi():
    if app.openapi_schema:
        return app.openapi_schema
    openapi_schema = get_openapi(
        title="Investment API",
        version="1.0.0",
        description="API com autenticação JWT",
        routes=app.routes,
    )
    
    openapi_schema["components"]["securitySchemes"] = {
        "BearerAuth": {
            "type": "http",
            "scheme": "bearer",
            "bearerFormat": "JWT",
        }
    }
    for path in openapi_schema["paths"].values():
        for method in path.values():
            method["security"] = [{"BearerAuth": []}]
    app.openapi_schema = openapi_schema
    return app.openapi_schema

app.openapi = custom_openapi

@app.on_event("startup")
async def startup():
    async with engine.begin() as conn:
        await conn.run_sync(models.Base.metadata.create_all)

@app.get("/")
async def root():
    return {"message": "API is running"}
