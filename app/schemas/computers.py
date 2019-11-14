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


class ProgramURL(BaseModel):
    upload_url: str


class ProgramFile(BaseModel):
    file: str  # noqa: WPS110


class FileReceiver(BaseModel):
    id: int
    owner_id: int


class FileInfo(BaseModel):
    doc: FileReceiver


class FileResponse(BaseModel):
    response: FileInfo
