from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DATABASE_URL: str
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_DB: str
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    SECRET_KEY: str
    KAFKA_CLIENT_ID: str
    KAFKA_BOOTSTRAP_SERVERS: list[str]
    ACCESS_TOKEN_EXPIRE_MINUTES: int
    REFRESH_TOKEN_EXPIRE_DAYS: int

    class Config:
        env_file = ".env"

settings = Settings()