from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    SECRET_KEY: str = "minha_chave_secreta_muito_forte_123456" 
    DATABASE_URL: str
    REDIS_URL: str

    class Config:
        env_file = ".env"

settings = Settings()
