from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ELASTICSEARCH_HOST: str
    ELASTICSEARCH_PORT: int
    SECRET_KEY: str
    KAFKA_CLIENT_ID: str
    KAFKA_BOOTSTRAP_SERVERS: list[str]
    class Config:
        env_file = ".env"

settings = Settings()