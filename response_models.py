from pydantic import BaseModel


class Computer(BaseModel):
    name: str
    username: str
    domain: str