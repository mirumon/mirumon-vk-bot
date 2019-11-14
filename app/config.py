import logging

from starlette.config import Config

from app.versions import get_app_version

logging.basicConfig(level=logging.DEBUG)

BOT_VERSION: str = get_app_version()

config = Config(".env")
DEBUG: bool = config("DEBUG", cast=bool, default=False)

TOKEN: str = config("TOKEN", cast=str)
CONFIRMATION_TOKEN: str = config("CONFIRMATION_TOKEN", cast=str)
GROUP_ID: int = config("GROUP_ID", cast=int)
SERVER_URL: str = config("SERVER_URL", cast=str)
SERVER_TIMEOUT: int = config("SERVER_TIMEOUT", cast=int, default=30)  # noqa: WPS432

API_VERSION: str = config("API_VERSION", cast=str, default="5.101")
BASE_VK_URL: str = config("BASE_VK_URL", cast=str, default="https://api.vk.com")
