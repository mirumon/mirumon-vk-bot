from enum import Enum

from pydantic import BaseModel


class Computer(BaseModel):
    name: str
    username: str
    domain: str


class Commands(str, Enum):  # noqa: WPS600
    computer_list: str = "computers"
