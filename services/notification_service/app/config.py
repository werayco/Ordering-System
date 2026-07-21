from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    SMTP_PORT: int
    
    class Config:
        env_file = ".env"

settings = Settings()