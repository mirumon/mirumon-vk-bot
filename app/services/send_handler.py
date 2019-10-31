import json

import requests
import vk
from typing import List

from app import config, resources
from app.resources import PROGRAMS_EXCEL_NAME
from app.schemas.computers import ProgramInfo
from app.services.mirumon_api import get_computers_list, get_programs_list
from app.services.utils import group_computers_by_domain, create_excel_file

api = vk.API(vk.Session(), v=config.API_VERSION)


def send_computer_list(user_id: int, computer_id: str):
    computer_list = get_computers_list()
    if computer_list:
        computers_group = group_computers_by_domain(computer_list)
        text = resources.COMPUTERS_LIST_TEMPLATE.render(computers_group=computers_group)
    else:
        text = resources.COMPUTERS_LIST_EMPTY_TEXT
    api.messages.send(
        access_token=config.TOKEN, user_id=user_id, random_id="", message=text)


def get_uploaded_file(url):
    response = requests.post(url, files={'file': open(PROGRAMS_EXCEL_NAME, 'rb')})
    result = json.loads(response.text)
    return result['file']


def get_attachable_file(file):
    request_path = f"https://api.vk.com/method/docs.save?file={file}&title=programs&tags=programs&v={config.API_VERSION}&access_token={config.TOKEN}"
    jsonAnswer = json.loads(requests.post(request_path).text)
    return f"doc{jsonAnswer['response']['doc']['owner_id']}_{jsonAnswer['response']['doc']['id']}"


def send_installed_programs(user_id: int, computer_id: int):
    programs_list: List[ProgramInfo] = get_programs_list(computer_id)
    create_excel_file(programs_list)

    upload_url = api.docs.getMessagesUploadServer(access_token=config.TOKEN, type='doc', peer_id=user_id)['upload_url']
    file = get_uploaded_file(upload_url)
    attach = get_attachable_file(file)

    api.messages.send(access_token=config.TOKEN,
                      user_id=user_id,
                      random_id="",
                      message=f"Программы, установленные на '{computer_id}' компьютере:",
                      attachment=attach)
