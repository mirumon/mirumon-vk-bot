from enum import Enum

from pydantic import BaseModel


class MessageType(str, Enum):
    message_new: str = "message_new"
    message_reply: str = "message_reply"
    message_result: str = "ok"
    confirmation: str = "confirmation"
    computer_list: str = "/computers"


class MessageSender(BaseModel):
    from_id: int
    text: str


class Message(BaseModel):
    type: MessageType
    object: MessageSender


class Registration(BaseModel):
    type: str
    group_id: int
