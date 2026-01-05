from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    database_dsn: str = Field(..., env="DATABASE_DSN")
   
    class Config:
        env_file = ".env"
