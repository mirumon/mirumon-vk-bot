from enum import Enum
from typing import Any, Callable, Dict, List

from app import resources
from app.resources import messages
from app.schemas.computers import ProgramInfo
from app.services import vk_api
from app.services.computers import group_computers_by_domain
from app.services.mirumon_api import BadResponse, get_computers_list, get_programs_list


class Commands(str, Enum):  # noqa: WPS600
    computer_list: str = "/computers"
    program_list: str = "/programs"


def handle_command(command: str, args: List[str], user_id: int) -> None:
    try:
        func = COMMANDS_HANDLERS[command]
    except KeyError:
        send_about_command_mistake(user_id)
    else:
        func(user_id=user_id, args=args)


def send_computer_list(user_id: int, **_: Any) -> None:
    computer_list = get_computers_list()
    if computer_list:
        computers_group = group_computers_by_domain(computer_list)
        text = messages.COMPUTERS_LIST_TEMPLATE.render(computers_group=computers_group)
    else:
        text = messages.NO_RUNNING_COMPUTERS
    vk_api.send_message(user_id=user_id, message=text)


def send_installed_programs(user_id: int, **kwargs: Any) -> None:
    try:
        computer_id: str = kwargs["args"][0]
    except IndexError:
        vk_api.send_message(user_id=user_id, message=messages.ENTER_COMPUTER_ID)
        return

    try:
        programs_list: List[ProgramInfo] = get_programs_list(computer_id)
    except BadResponse as exception:
        text = str(exception)
        attach = None
    else:
        text = messages.INSTALLED_PROGRAMS_ON_DEVICE_TEMPLATE.render(
            computer_id=computer_id
        )
        attach = vk_api.get_attachable_file(
            programs_list, resources.PROGRAMS_EXCEL_NAME, user_id
        )

    vk_api.send_message(user_id=user_id, message=text, attachment=attach)


def send_about_command_mistake(user_id: int) -> None:
    vk_api.send_message(user_id=user_id, message=messages.ENTERED_UNKNOWN_COMMAND)


COMMANDS_HANDLERS: Dict[str, Callable] = {  # noqa: WPS407
    Commands.computer_list: send_computer_list,
    Commands.program_list: send_installed_programs,
}
