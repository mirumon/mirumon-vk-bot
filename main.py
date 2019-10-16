from typing import Union

import requests
import starlette
import vk
from fastapi import FastAPI, HTTPException

import config
from message_handler import *
from response_models import *

app = FastAPI()
session = vk.Session()
api = vk.API(session, v=config.API_VERSION)


@app.post("/callback")
def vk_callback(event: Union[Message, Registration]):
    if event.type == MessageType.confirmation and event.group_id == config.GROUP_ID:
        return config.CONFIRMATION_TOKEN
    if event.type == MessageType.message_new:
        user_id = event.object.from_id
        user_message = event.object.text
        bot_message = ''
        if user_message == MessageType.computer_list:
            resp = requests.get(config.SERVER_URL + user_message)
            computers = [Computer(**current) for current in resp.json()]
            sorted(computers, key=lambda v: v.domain)
            for computer in computers:
                bot_message += "\n".join([
                    f"In domain '{computer.domain}'",
                    f"{computer.name} [{computer.username}]\n"])
            api.messages.send(access_token=config.TOKEN, user_id=user_id, random_id='', message=bot_message)
            return MessageType.message_result
    raise HTTPException(status_code=starlette.status, detail={"error": f"event '{event.type}' not supported"})
