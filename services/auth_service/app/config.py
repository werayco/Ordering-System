from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    REDIS_HOST: str
    REDIS_PORT: int
    SECRET_KEY: str
    ADMIN_COUNT: int
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int
    class Config:
        env_file = ".env"

settings = Settings()