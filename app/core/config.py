from functools import lru_cache

from pydantic_settings import BaseSettings


class Settings(BaseSettings):

    APP_NAME: str = "SCALABLE RAG"

    APP_VERSION: str = "1.0.0"

    DEBUG: bool = True

    HOST: str = "0.0.0.0"

    PORT: int = 8000

    GROQ_API_KEY: str

    class Config:
        env_file = ".env"


@lru_cache
def get_settings():
    return Settings()