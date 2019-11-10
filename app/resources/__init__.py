from mako.lookup import TemplateLookup

_TEMPLATE_LOOKUP = TemplateLookup(directories=["app/resources"], input_encoding="utf-8")

COMPUTERS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("computers_message.mako")
PROGRAMS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("programs_message.mako")
COMPUTERS_LIST_FAILED_TEXT = "Ошибка сервера"
COMPUTERS_LIST_EMPTY_TEXT = "Нет активных компьютеров"
PROGRAMS_LIST_TIMEOUT_TEXT = "Ошибка ожидания сервера"
EVENT_ERROR_TEXT = "Ивент не поддерживается"
PROGRAMS_EXCEL_NAME = "programs.xlsx"
BASE_VK_URL = "https://api.vk.com"
DOCS_SAVE_ENDPOINT = "/method/docs.save"
