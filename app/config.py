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
API_VERSION: str = config("API_VERSION", cast=str, default="5.101")
COMPUTERS_LIST_FAILED_TEXT: str = config("COMPUTERS_LIST_FAILED_TEXT", cast=str)
COMPUTERS_LIST_EMPTY_TEXT: str = config("COMPUTERS_LIST_EMPTY_TEXT", cast=str)
PROGRAMS_LIST_TIMEOUT_TEXT: str = config("PROGRAMS_LIST_TIMEOUT_TEXT", cast=str)
EVENT_ERROR_TEXT: str = config("EVENT_ERROR_TEXT", cast=str)
PROGRAMS_EXCEL_NAME: str = config("PROGRAMS_EXCEL_NAME", cast=str)
BASE_VK_URL: str = config("BASE_VK_URL", cast=str)
DOCS_SAVE_ENDPOINT: str = config("DOCS_SAVE_ENDPOINT", cast=str)
SERVER_TIMEOUT: int = config("SERVER_TIMEOUT", cast=int)
