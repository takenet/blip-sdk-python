from uuid import uuid4

import lime_python


class Application:
    """Basic Application with default values."""

    def __init__(self) -> None:
        self.identifier = str(uuid4())
        self.compression = lime_python.SessionCompression.NONE
        self.encryption = lime_python.SessionEncryption.NONE
        self.instance = 'default'
        self.domain = 'msging.net'
        self.scheme = 'wss'
        self.hostname = 'ws.msging.net'
        self.port = 443
        self.precense = {
            'status': 'available',
            'routingRule': 'identity'
        }
        self.notify_consumed = True
        self.authentication = lime_python.GuestAuthentication()
        self.command_timeout = 6  # in seconds
