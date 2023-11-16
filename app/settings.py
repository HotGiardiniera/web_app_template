from functools import cache

from pydantic import Extra, SecretStr
from pydantic_settings import BaseSettings


@cache
def settings():
    return Settings()


class Settings(BaseSettings):
    flask_secret: str = 'secret'
    base_url: str = 'http://0.0.0.0/'

    connection_string: str = 'sqlite://'
    ro_connection_string: str = 'sqlite://'

    google_oauth_client_id: str = ''
    google_oauth_client_secret: str = ''

    jwt_private_key: SecretStr = "SUPER SECRET"
    jwt_kid: str = 'CHRIS_SIGNING_KEY'

    class Config:
        case_sensitive = False
        env_file = '.env'
        extra = Extra.ignore
