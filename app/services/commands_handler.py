from enum import Enum

from app.services.send_handler import send_computer_list, send_installed_programs


class Commands(str, Enum):  # noqa: WPS600
    computer_list: str = "/computers"
    program_list: str = "/programs"


def handle_command(command: str, arg: str, user_id: int):
    func = COMMANDS_HANDLERS[command]  # TODO check null ptr
    func(user_id=user_id, computer_id=arg)


COMMANDS_HANDLERS = {
    Commands.computer_list: send_computer_list,
    Commands.program_list: send_installed_programs,
}
