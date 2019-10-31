from pydantic import BaseModel


class ComputerItem(BaseModel):
    mac_address: str
    name: str
    username: str
    domain: str


class ProgramInfo(BaseModel):
    name: str
    vendor: str
    version: str
