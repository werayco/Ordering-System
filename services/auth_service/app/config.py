from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    REDIS_HOST: str
    REDIS_PORT: int
    SECRET_KEY: str
    ADMIN_COUNT: int
    class Config:
        env_file = ".env"

settings = Settings()