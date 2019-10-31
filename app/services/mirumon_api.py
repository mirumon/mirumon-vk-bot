import requests
from starlette.status import HTTP_200_OK
from typing import List

from app import config
from app.schemas.computers import ComputerItem, ProgramInfo


def get_computers_list() -> List[ComputerItem]:
    response = requests.get(f"{config.SERVER_URL}/computers")
    if response.status_code != HTTP_200_OK:
        raise RuntimeError("Server bad response")
    return [ComputerItem(**current) for current in response.json()]


def get_programs_list(computer_id: str) -> List[ProgramInfo]:
    response = requests.get(f"{config.SERVER_URL}/computers/{computer_id}/installed-programs")
    if response.status_code != HTTP_200_OK:
        raise RuntimeError("Server bad response")
    return [ProgramInfo(**current) for current in response.json()]
