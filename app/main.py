from typing import Dict, List, Union

import requests
import vk
from fastapi import FastAPI, HTTPException
from starlette.status import HTTP_200_OK, HTTP_400_BAD_REQUEST

from app import config, resources
from app.schemas.computer import Commands, Computer
from app.schemas.messages import Message, MessageType, Registration

app = FastAPI()
session = vk.Session()
api = vk.API(session, v=config.API_VERSION)


def get_computers_list() -> List[Computer]:
    response = requests.get(f"{config.SERVER_URL}/computers")
    if response.status_code != HTTP_200_OK:
        raise RuntimeError("Server bad response")
    return [Computer(**current) for current in response.json()]


def group_computers_by_domain(computers: List[Computer]) -> Dict[str, List[Computer]]:
    computer_group: Dict[str, List[Computer]] = {}
    for computer in computers:
        if computer.domain in computer_group:
            computer_group[computer.domain].append(computer)
        else:
            computer_group[computer.domain] = [computer]
    return computer_group


@app.post("/callback")
def vk_callback(event: Union[Message, Registration]) -> str:
    if event.type == MessageType.confirmation and event.group_id == config.GROUP_ID:
        return config.CONFIRMATION_TOKEN

    user_message = event.object.text
    user_id = event.object.from_id

    if event.type != MessageType.message_new and user_message != Commands.computer_list:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=resources.EVENT_ERROR_TEXT
        )
    try:
        computers = get_computers_list()
    except RuntimeError:
        api.messages.send(
            access_token=config.TOKEN,
            user_id=user_id,
            random_id="",
            message=resources.COMPUTERS_LIST_FAILED_TEXT,
        )
        return MessageType.message_result
    if computers:
        computers_group = group_computers_by_domain(computers)
        text = resources.COMPUTERS_LIST_TEMPLATE.render(computers_group=computers_group)
    else:
        text = resources.COMPUTERS_LIST_EMPTY_TEXT
    api.messages.send(
        access_token=config.TOKEN, user_id=user_id, random_id="", message=text
    )
    return MessageType.message_result
