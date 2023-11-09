from functools import cache

from pydantic import Extra
from pydantic_settings import BaseSettings


@cache
def settings():
    return Settings()


class Settings(BaseSettings):
    connection_string: str = 'sqlite://'
    ro_connection_string: str = 'sqlite://'

    class Config:
        case_sensitive = False
        env_file = '.env'
        extra = Extra.ignore
