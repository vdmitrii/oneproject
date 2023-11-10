import logging
from functools import lru_cache

from pydantic import AnyUrl, BaseSettings

log = logging.getLogger("uvicorn")


class Settings(BaseSettings):
    environment = "dev"
    testing = 0
    model_url = None


@lru_cache()
def get_settings():
    log.info("Loading config settings from the environment...")
    return Settings()
