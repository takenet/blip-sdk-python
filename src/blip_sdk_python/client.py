from asyncio import Future
from typing import Callable, Dict
from lime_python import Transport
from .application import Application
from .extensions.extension_base import ExtensionBase
from .utilities import ClassUtilities

MAX_CONNECTION_TRY_COUNT = 10


class Client:
    """blip API Client."""

    def __init__(
        self,
        uri: str,
        transport_factory: Callable[[], Transport],
        application: Application
    ) -> None:

        default_application = Application()
        self.application: Application = ClassUtilities.merge_dataclasses(
            default_application,
            application
        )

        self.__message_receivers: list = []
        self.__notification_receivers: list = []
        self.__command_receivers: list = []
        self.__command_resolves: list = []
        self.session_future: Future = Future()
        self.session_finished_handlers: list = []
        self.session_failed_handlers: list = []

        self.__listening: bool = False
        self.__closing: bool = False
        self.__uri: str = uri
        self.__connection_try_count: int = 0

        if isinstance(transport_factory, Transport):
            transport_factory = lambda: transport_factory

        self.__transport_factory: Callable[[], Transport] = transport_factory

        self._extensions: Dict[type, ExtensionBase] = {}

        self.initialize_client_channel()

    def initialize_client_channel(self) -> None:
        """Initialize the transport client."""
        pass
