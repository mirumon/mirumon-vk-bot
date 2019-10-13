from enum import Enum
from typing import Union

import vk
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

import config


class MessageSender(BaseModel):
    from_id: int


class EventType(str, Enum):
    message_new: str = "message_new"
    message_reply: str = "message_reply"
    confirmation: str = "confirmation"
    ok: str = "ok"


class Message(BaseModel):
    type: EventType
    object: MessageSender


class VkRegistration(BaseModel):
    type: str
    group_id: int


app = FastAPI()
session = vk.Session()
api = vk.API(session, v=5.101)


@app.post("/callback")
async def vk_callback(event: Union[Message, VkRegistration]):
    if event.type == EventType.confirmation and event.group_id == config.GROUP_ID:
        return config.CONFIRMATION_TOKEN
    if event.type == EventType.message_new:
        user_id = event.object.from_id
        api.messages.send(access_token=config.TOKEN, user_id=user_id, random_id='', message='Hi there!')
        return EventType.ok
    raise HTTPException(status_code=400, detail={"error": f"event '{event.type}' not supported"})
