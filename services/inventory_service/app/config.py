from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    SECRET_KEY: str
    KAFKA_CLIENT_ID: str
    KAFKA_BOOTSTRAP_SERVERS: list[str]
    class Config:
        env_file = ".env"

settings = Settings()