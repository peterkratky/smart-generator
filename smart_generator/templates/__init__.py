from .templates_provider import TemplatesProvider

templates_provider = None


def set_templates_provider(provider):
    global templates_provider
    templates_provider = provider


def get_templates_provider():
    global templates_provider
    return templates_provider
