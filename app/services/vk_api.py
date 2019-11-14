import logging
from io import BytesIO
from random import randint
from typing import List, Optional

import httpx
import vk

from app import config
from app.config import BASE_VK_URL
from app.schemas.computers import FileResponse, ProgramFile, ProgramInfo, ProgramURL
from app.schemas.vk_messages import Registration
from app.services.excel import create_excel_file

api = vk.API(vk.Session(), v=config.API_VERSION)


def send_message(user_id: int, message: str, attachment: Optional[str] = None) -> None:
    api.messages.send(
        access_token=config.TOKEN,
        user_id=user_id,
        random_id=_get_random_id(),
        message=message,
        attachment=attachment,
    )


def _get_attachable_endpoint(filename: str) -> str:
    request_path = f"{BASE_VK_URL}/method/docs.save"
    query_params = {
        "file": filename,
        "title": "programs",
        "tags": "programs",
        "v": config.API_VERSION,
        "access_token": config.TOKEN,
    }
    json_result = httpx.get(request_path, params=query_params).json()
    about_file = FileResponse.parse_obj(json_result)
    return f"doc{about_file.response.doc.owner_id}_{about_file.response.doc.id}"


def get_uploaded_file(url: str, document: BytesIO) -> str:
    response = httpx.post(url, files={"file": document})
    json_result = response.json()
    logging.debug(json_result)
    return ProgramFile.parse_obj(json_result).file


def get_attachable_file(
    programs_list: List[ProgramInfo], filename: str, user_id: int
) -> str:
    programs_file = create_excel_file(programs_list, filename)
    upload_dict = api.docs.getMessagesUploadServer(
        access_token=config.TOKEN, type="doc", peer_id=user_id
    )
    url_object = ProgramURL(**upload_dict)
    new_file = get_uploaded_file(url_object.upload_url, programs_file)
    return _get_attachable_endpoint(new_file)


def check_group_id(event: Registration) -> bool:
    return event.group_id == config.GROUP_ID


def _get_random_id() -> int:
    first_rand_value = 1
    last_rand_value = 1_000_000
    return randint(first_rand_value, last_rand_value)  # noqa: S311
