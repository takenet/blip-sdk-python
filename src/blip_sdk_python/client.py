from asyncio import Future
from time import sleep
from typing import Any, Callable, Dict, List

from lime_python import (ClientChannel, Command, Envelope, Message,
                         Notification, NotificationEvent, Session, Transport)

from .application import Application
from .extensions.extension_base import ExtensionBase
from .receiver import Receiver
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

        self.__message_receivers: List[Receiver] = []
        self.__notification_receivers: List[Receiver] = []
        self.__command_receivers: List[Receiver] = []
        self.__command_resolves: list = []
        self.session_future: Future = None
        self.session_finished_handlers: List[Callable[[Session], None]] = []
        self.session_failed_handlers: List[Callable[[Session], None]] = []

        self.__listening: bool = False
        self.__closing: bool = False
        self.__uri: str = uri
        self.__connection_try_count: int = 0

        if isinstance(transport_factory, Transport):
            transport_factory = lambda: transport_factory

        self.__transport_factory: Callable[[], Transport] = transport_factory
        self.__transport: Transport = None

        self.__client_channel: ClientChannel = None

        self._extensions: Dict[type, ExtensionBase] = {}

        self.initialize_client_channel()

    def initialize_client_channel(self) -> None:
        """Initialize client channel listeners."""
        self.__transport.on_close = self.__transport_on_close

        self.session_future = Future()

        self.__client_channel = ClientChannel(self.__transport, True, False)
        self.__client_channel.on_message = self.__client_channel_on_message
        self.__client_channel.on_notification = self.__client_channel_on_notification  # noqa: E501
        self.__client_channel.on_command = self.__client_channel_on_command
        self.__client_channel.on_session_finished = self.__client_channel_on_session_finished  # noqa: E501
        self.__client_channel.on_session_failed = self.__client_channel_on_session_failed  # noqa: E501

    def __client_channel_on_session_finished(self, session: Session) -> None:
        self.session_future.set_result(session)
        self.__notify_handlers(self.session_finished_handlers, session)

    def __client_channel_on_session_failed(self, session: Session) -> None:
        self.session_future.set_exception(session)
        self.__notify_handlers(self.session_failed_handlers, session)

    def __notify_handlers(
        self,
        handler_list: List[Callable[[Envelope], None]],
        envelope: Envelope
    ) -> None:
        for handler in handler_list:
            handler(envelope)

    def __client_channel_on_command(
        self,
        command: Command
    ) -> None:
        resolve = self.__command_resolves[command.id]
        resolve = resolve if resolve else self.__reflect
        resolve(command)

        self.__notify_receivers(self.__command_receivers, command)

    def __client_channel_on_notification(
        self,
        notification: Notification
    ) -> None:
        self.__notify_receivers(self.__notification_receivers, notification)

    def __notify_receivers(
        self,
        receiver_list: List[Receiver],
        envelope: Envelope
    ) -> None:
        [   # noqa: WPS428
            receiver.callback(envelope)
            for receiver in receiver_list
            if receiver.predicate(envelope)
        ]

    def __client_channel_on_message(self, message: Message) -> None:
        should_notify = message.id and (
            not message.to or
            self.__client_channel.local_node.lower().startswith(
                message.to.lower()
            )
        )

        if should_notify:
            notification = Notification(NotificationEvent.RECEIVED)
            notification.id = message.id
            notification.to = message.pp if message.pp else message.from_n
            notification.metadata = {
                '#message.to': message.to
            }
            self.send_notification(notification)

        self.__loop(0, should_notify, message)

    def __transport_on_close(self) -> None:
        self.__listening = False
        if not self.__closing:
            # Use an exponential backoff for the timeout in seconds
            timeout = (100 * (2 ** self.__connection_try_count)) / 1000.0

            # Try to reconnect after the timeout
            sleep(timeout)
            if not self.__closing:
                self.__transport = self.__transport_factory()
                self.initialize_client_channel()
                self.connect()

    def __loop(
        self,
        index: int,
        should_notify: bool,
        message: Message
    ) -> None:
        pass

    def __reflect(self, any: Any) -> Any:
        return any
