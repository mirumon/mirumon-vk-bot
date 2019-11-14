from typing import List

import httpx
import vk

from app import config
from app.config import (
    BASE_VK_URL,
    COMPUTERS_LIST_EMPTY_TEXT,
    DOCS_SAVE_ENDPOINT,
    PROGRAMS_EXCEL_NAME,
    UNKNOWN_COMMAND,
)
from app.resources import COMPUTERS_LIST_TEMPLATE
from app.schemas.computers import FileResponse, ProgramFile, ProgramInfo, ProgramURL
from app.services.mirumon_api import BadResponse, get_computers_list, get_programs_list
from app.services.utils import create_excel_file, group_computers_by_domain

api = vk.API(vk.Session(), v=config.API_VERSION)


def send_computer_list(user_id: int, random_id: int, computer_id: str) -> None:
    computer_list = get_computers_list()
    if computer_list:
        computers_group = group_computers_by_domain(computer_list)
        text = COMPUTERS_LIST_TEMPLATE.render(computers_group=computers_group)
    else:
        text = COMPUTERS_LIST_EMPTY_TEXT
    api.messages.send(
        access_token=config.TOKEN,
        user_id=user_id,
        random_id=random_id,
        message=text
    )


def get_uploaded_file(url: str) -> str:
    response = httpx.post(url, files={'file': open(PROGRAMS_EXCEL_NAME, 'rb')})  # noqa: Q000
    json_result = response.json()
    return ProgramFile.parse_obj(json_result).file


def get_attachable_endpoint(new_file: str) -> str:
    request_path = BASE_VK_URL + DOCS_SAVE_ENDPOINT
    query_params = {'file': new_file,
                    'title': "programs",
                    'tags': "programs",
                    'v': config.API_VERSION,
                    'access_token': config.TOKEN
                    }

    json_result = httpx.get(request_path, params=query_params).json()
    about_file = FileResponse.parse_obj(json_result)
    return f"doc{about_file.response.doc.owner_id}_{about_file.response.doc.id}"


def get_attachable_file(programs_list: List[ProgramInfo], user_id: int) -> str:
    create_excel_file(programs_list)
    upload_dict = api.docs.getMessagesUploadServer(
        access_token=config.TOKEN,
        type='doc',
        peer_id=user_id
    )
    url_object = ProgramURL(**upload_dict)
    new_file = get_uploaded_file(url_object.upload_url)
    return get_attachable_endpoint(new_file)


def send_installed_programs(user_id: int, random_id: int, computer_id: str) -> None:
    try:
        programs_list: List[ProgramInfo] = get_programs_list(computer_id)
    except BadResponse as exception:
        text = str(exception)
        attach = ''
    else:
        text = f"Программы, установленные на '{computer_id}' компьютере:"
        attach = get_attachable_file(programs_list, user_id)

    api.messages.send(access_token=config.TOKEN,
                      user_id=user_id,
                      random_id=random_id,
                      message=text,
                      attachment=attach
                      )


def send_about_command_mistake(user_id: int, random_id: int) -> None:
    api.messages.send(access_token=config.TOKEN,
                      user_id=user_id,
                      random_id=random_id,
                      message=UNKNOWN_COMMAND
                      )
