from mako.lookup import TemplateLookup

_TEMPLATE_LOOKUP = TemplateLookup(directories=["app/resources"], input_encoding="utf-8")

COMPUTERS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("computers_message.mako")
PROGRAMS_LIST_TEMPLATE = _TEMPLATE_LOOKUP.get_template("programs_message.mako")
