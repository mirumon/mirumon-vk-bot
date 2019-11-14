from typing import Union, cast

from fastapi import FastAPI, HTTPException
from starlette.responses import PlainTextResponse
from starlette.status import HTTP_400_BAD_REQUEST

from app import config
from app.resources import messages
from app.schemas.vk_messages import Message, MessageType, Registration
from app.services.commands_handler import handle_command
from app.services.vk_api import check_group_id

app = FastAPI(title="Mirumon VK Bot", version=config.BOT_VERSION, debug=config.DEBUG)


@app.post("/callback", response_class=PlainTextResponse)
def vk_callback(event: Union[Message, Registration]) -> str:
    if event.type == MessageType.confirmation:
        if check_group_id(cast(Registration, event)):
            return config.CONFIRMATION_TOKEN

    if event.type != MessageType.message_new:
        raise HTTPException(
            status_code=HTTP_400_BAD_REQUEST,
            detail=messages.FUNCTION_NOT_IMPLEMENTED_ON_DEVICE,
        )

    event = cast(Message, event)
    user_id = event.object.from_id

    try:
        command, *args = event.object.text.split()
    except ValueError:
        command, args = event.object.text, []

    handle_command(command, args, user_id)

    return MessageType.message_result
