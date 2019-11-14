from typing import List

import httpx
from httpx import ReadTimeout
from starlette.status import HTTP_200_OK

from app import config
from app.schemas.computers import ComputerItem, ProgramInfo


class BadResponse(Exception):
    pass  # noqa: WPS 604


client = httpx.Client(base_url=config.SERVER_URL)


def get_computers_list() -> List[ComputerItem]:
    response = client.get("/computers")
    if response.status_code != HTTP_200_OK:
        raise BadResponse(f"Server bad response, status code: {response.status_code}")
    return [ComputerItem(**program) for program in response.json()]


def get_programs_list(computer_id: str) -> List[ProgramInfo]:
    try:
        response = client.get(f"/computers/{computer_id}/installed-programs",
                              timeout=config.SERVER_TIMEOUT
                              )
    except ReadTimeout:
        raise BadResponse("Server Timeout")
    if response.status_code != HTTP_200_OK:
        raise BadResponse(f"Server bad response, status code: {response.status_code}")
    return [ProgramInfo(**program) for program in response.json()]
