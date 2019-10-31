from fastapi import FastAPI, HTTPException
from starlette.responses import PlainTextResponse
from starlette.status import HTTP_400_BAD_REQUEST
from typing import Union, cast

from app import config, resources
from app.schemas.messages import Message, MessageType, Registration
from app.services.commands_handler import handle_command
from app.services.utils import check_group_id

app = FastAPI()


@app.post("/callback", response_class=PlainTextResponse)
def vk_callback(event: Union[Message, Registration]) -> str:
    if event.type == MessageType.confirmation:
        if check_group_id(cast(Registration, event)):
            return config.CONFIRMATION_TOKEN

    if event.type != MessageType.message_new:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST, detail=resources.EVENT_ERROR_TEXT
        )

    event = cast(Message, event)
    user_id = event.object.from_id
    try:
        command, computer_id = event.object.text.split(" ", 1)
    except ValueError:
        command = event.object.text
        computer_id = ""

    handle_command(command, computer_id.strip(), user_id)

    return MessageType.message_result
