import logging

from starlette.config import Config

logging.basicConfig(level=logging.DEBUG)

config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

TOKEN: str = config("TOKEN", cast=str)
CONFIRMATION_TOKEN: str = config("CONFIRMATION_TOKEN", cast=str)
GROUP_ID: int = config("GROUP_ID", cast=int)
SERVER_URL: str = config("SERVER_URL", cast=str)
API_VERSION: str = config("API_VERSION", cast=str, default="5.101")
