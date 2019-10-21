from mako.lookup import TemplateLookup

_TEMPLATE_LOOKUP = TemplateLookup(directories=["app/resources"], input_encoding="utf-8")

COMPUTERS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("computers_message.mako")
COMPUTERS_LIST_FAILED_TEXT = "Server error"
COMPUTERS_LIST_EMPTY_TEXT = "No computers"
EVENT_ERROR_TEXT = "event not supported"
