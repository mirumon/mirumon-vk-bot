from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):  # noqa: WPS600
    message_new: str = "message_new"
    message_reply: str = "message_reply"
    message_result: str = "ok"
    confirmation: str = "confirmation"


class MessageSender(BaseModel):
    from_id: int
    text: str


class Message(BaseModel):
    type: MessageType
    object: MessageSender


class Registration(BaseModel):
    type: str
    group_id: int
