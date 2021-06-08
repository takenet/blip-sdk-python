from typing import Dict

from lime_python import Command


class SESSIONS:
    authenticating: Dict[str, str] = {
        'id': '0',
        'from': '127.0.0.1:8124',
        'state': 'authenticating'
    }
    established: Dict[str, str] = {
        'id': '0',
        'from': '127.0.0.1:8124',
        'state': 'established'
    }


class MESSAGES:
    pong: Dict[str, str] = {
        'type': 'text/plain',
        'content': 'pong'
    }


class NOTIFICATIONS:
    pong: Dict[str, str] = {
        'event': 'pong'
    }


class COMMANDS:

    @staticmethod
    def ping_response(envelope: Command) -> Command:
        return {'id': envelope.id, 'method': 'get', 'status': 'success'}
