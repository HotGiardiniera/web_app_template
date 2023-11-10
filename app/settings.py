from functools import cache

from pydantic import Extra
from pydantic_settings import BaseSettings


@cache
def settings():
    return Settings()


class Settings(BaseSettings):
    flask_secret: str = 'secret'
    connection_string: str = 'sqlite://'
    ro_connection_string: str = 'sqlite://'
    google_oauth_client_id: str = ''
    google_oauth_client_secret: str = ''

    class Config:
        case_sensitive = False
        env_file = '.env'
        extra = Extra.ignore
