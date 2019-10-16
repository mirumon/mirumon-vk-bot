import logging

from starlette.config import Config

logging.basicConfig(level=logging.DEBUG)

config = Config(".env")
DEBUG = config("DEBUG", cast=bool, default=False)

TOKEN = config("TOKEN", cast=str)
CONFIRMATION_TOKEN = config("CONFIRMATION_TOKEN", cast=str)
GROUP_ID = config("GROUP_ID", cast=int)
SERVER_URL = config("SERVER_URL", cast=str)
