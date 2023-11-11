import logging
from functools import lru_cache

from pydantic import AnyUrl
from pydantic_settings import BaseSettings, SettingsConfigDict

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment: str = "dev"
    testing: int = 0
    model_urlL: AnyUrl = None


@lru_cache()
def get_settings():
    log.info("Loading config settings from the environment...")
    return Settings()
