import json

import httpx
import vk
from typing import List

from app import config
from app.resources import PROGRAMS_EXCEL_NAME, COMPUTERS_LIST_TEMPLATE, \
    COMPUTERS_LIST_EMPTY_TEXT, BASE_VK_URL, DOCS_SAVE_ENDPOINT
from app.schemas.computers import ProgramInfo
from app.services.mirumon_api import get_computers_list, get_programs_list, BadResponse
from app.services.utils import group_computers_by_domain, create_excel_file

api = vk.API(vk.Session(), v=config.API_VERSION)


def send_computer_list(user_id: int, random_id: int, computer_id: str):
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
        message=text)


def get_uploaded_file(url):
    response = httpx.post(url, files={'file': open(PROGRAMS_EXCEL_NAME, 'rb')})
    result = json.loads(response.text)
    return result['file']


def get_attachable_file(file):
    request_path = BASE_VK_URL + DOCS_SAVE_ENDPOINT
    params = {'file': file,
              'title': "programs",
              'tags': "programs",
              'v': config.API_VERSION,
              'access_token': config.TOKEN
              }

    json_answer = httpx.get(request_path, params=params).json()
    about_file = json_answer['response']['doc']
    return f"doc{about_file['owner_id']}_{about_file['id']}"


def send_installed_programs(user_id: int, random_id: int, computer_id: int):
    try:
        programs_list: List[ProgramInfo] = get_programs_list(computer_id)
        text = f"Программы, установленные на '{computer_id}' компьютере:"
        create_excel_file(programs_list)
        upload_url = api.docs.getMessagesUploadServer(
            access_token=config.TOKEN,
            type='doc',
            peer_id=user_id)['upload_url']

        file = get_uploaded_file(upload_url)
        attach = get_attachable_file(file)

    except BadResponse as exception:
        text = exception
        attach = ''

    print(random_id)
    api.messages.send(access_token=config.TOKEN,
                      user_id=user_id,
                      random_id=random_id,
                      message=text,
                      attachment=attach
                      )
