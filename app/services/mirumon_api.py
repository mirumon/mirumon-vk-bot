import httpx
from starlette.status import HTTP_200_OK
from typing import List

from app import config
from app.schemas.computers import ComputerItem, ProgramInfo


class BadResponse(Exception):
    def __init__(self, *args, **kwargs):  # real signature unknown
        pass


client = httpx.Client(base_url=config.SERVER_URL)


def get_computers_list() -> List[ComputerItem]:
    response = client.get("/computers")
    if response.status_code != HTTP_200_OK:
        raise BadResponse(f"Server bad response, status code: {response.status_code}")
    return [ComputerItem(**current) for current in response.json()]


def get_programs_list(computer_id: str) -> List[ProgramInfo]:
    try:
        response = client.get(f"/computers/{computer_id}/installed-programs", timeout=15)
    except client.exceptions.ReadTimeout:
        raise BadResponse("Server Timeout")
    if response.status_code != HTTP_200_OK:
        raise BadResponse(f"Server bad response, status code: {response.status_code}")
    return [ProgramInfo(**current) for current in response.json()]
