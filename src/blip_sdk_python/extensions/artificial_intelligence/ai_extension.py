from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates
from .content_type import ContentType
from lime_python.protocol.command import Command

POSTMASTER_AI = 'postmaster@ai'


class AiExtension(ExtensionBase):
    """Extension to handle Blip AI Services"""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    def get_analysis(self):
        pass
