from dataclasses import dataclass, field
from typing import Dict
from uuid import uuid4

from lime_python import (Authentication, GuestAuthentication,
                         SessionCompression, SessionEncryption)


@dataclass
class Application:
    """Basic Application with default values."""

    identifier: str = str(uuid4())
    compression: str = SessionCompression.NONE
    encryption: str = SessionEncryption.NONE
    instance: str = 'default'
    domain: str = 'msging.net'
    scheme: str = 'wss'
    hostname: str = 'ws.msging.net'
    port: int = 443
    presence: Dict[str, str] = field(
        default_factory=lambda: {
            'status': 'available',
            'routingRule': 'identity'
        }
    )
    notify_consumed: bool = True
    authentication: Authentication = GuestAuthentication()
    command_timeout: int = 6  # in seconds
