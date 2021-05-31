from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4

import lime_python


@dataclass(frozen=True)
class Application:
    """Basic Application with default values."""

    identifier: str = str(uuid4())
    compression: str = lime_python.SessionCompression.NONE
    encryption: str = lime_python.SessionEncryption.NONE
    instance: str = 'default'
    domain: str = 'msging.net'
    scheme: str = 'wss'
    hostname: str = 'ws.msging.net'
    port: int = 443
    presence: Dict[str, str] = field(default_factory=lambda: {
        'status': 'available',
        'routingRule': 'identity'
    })
    notify_consumed: bool = True
    authentication: lime_python.GuestAuthentication = \
        lime_python.GuestAuthentication()
    command_timeout: int = 6  # in seconds
