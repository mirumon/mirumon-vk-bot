from enum import Enum
from typing import Callable, Dict

from app.services.send_handler import (
    send_about_command_mistake,
    send_computer_list,
    send_installed_programs,
)


class Commands(str, Enum):  # noqa: WPS600
    computer_list: str = "/computers"
    program_list: str = "/programs"


def handle_command(command: str, arg: str, user_id: int, random_id: int) -> None:
    try:
        func = COMMANDS_HANDLERS[command]
    except KeyError:
        send_about_command_mistake(user_id, random_id)
    else:
        func(user_id=user_id, computer_id=arg, random_id=random_id)


COMMANDS_HANDLERS: Dict[str, Callable] = {
    Commands.computer_list: send_computer_list,
    Commands.program_list: send_installed_programs,
}
