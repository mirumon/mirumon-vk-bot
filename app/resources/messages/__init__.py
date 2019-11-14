from mako.lookup import TemplateLookup
from mako.template import Template

_TEMPLATE_LOOKUP = TemplateLookup(directories=["app/resources"], input_encoding="utf-8")

COMPUTERS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("computers_message.mako")

INSTALLED_PROGRAMS_ON_DEVICE_TEMPLATE = Template(
    "Программы, установленные на '${ computer_id }' компьютере:"
)

ENTER_COMPUTER_ID = "Введите идентификатор компьютера"

SERVER_ERROR = "Ошибка сервера"
NO_RUNNING_COMPUTERS = "Нет запущенных компьютеров"
SERVER_TIMEOUT = "Ошибка ожидания сервера"

FUNCTION_NOT_IMPLEMENTED_ON_DEVICE = "Данная функция не поддерживается устройством"
ENTERED_UNKNOWN_COMMAND = "Введена неизвестная команда"
