from asyncio import Future, ensure_future, get_event_loop
from time import sleep
from typing import Any, Callable, Dict, List, Type

from lime_python import (ClientChannel, Command, CommandMethod, Envelope,
                         GuestAuthentication, KeyAuthentication, Message,
                         Notification, NotificationEvent, PlainAuthentication,
                         Reason, ReasonCode, Session, SessionState, Transport)

from .application import Application
from .extensions import (AiExtension, ChatExtension, ExtensionBase,
                         MediaExtension)
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

        self.session_future: Future = None
        self.__message_receivers: List[Receiver] = []
        self.__notification_receivers: List[Receiver] = []
        self.__command_receivers: List[Receiver] = []
        self.__command_resolves: Dict[str, Callable] = {}
        self.__session_finished_handlers: List[Callable[[Session], None]] = []
        self.__session_failed_handlers: List[Callable[[Session], None]] = []

        self.uri: str = uri
        self.__listening: bool = False
        self.__closing: bool = False
        self.__connection_try_count: int = 0

        if isinstance(transport_factory, Transport):
            transport_factory = lambda: transport_factory

        self.transport: Transport = transport_factory()
        self.__transport_factory: Callable[[], Transport] = transport_factory

        self.client_channel: ClientChannel = None

        self.__extensions: Dict[Type, ExtensionBase] = {}

        self.__initialize_client_channel()

    @property
    def chat_extension(self) -> ChatExtension:  # noqa: D102
        return self.__get_extension(ChatExtension)

    @property
    def media_extension(self) -> MediaExtension:  # noqa: D102
        return self.__get_extension(MediaExtension, self.application.domain)

    @property
    def ai_extension(self) -> AiExtension:  # noqa: D102
        return self.__get_extension(AiExtension, self.application.domain)

    @property
    def listening(self) -> bool:  # noqa: D102
        return self.__listening

    @listening.setter
    def listening(self, value: bool):
        self.__listening = value
        self.on_listening_changed(value)

    async def connect_with_guest_async(self, identifier: str) -> Session:
        """Connect using Guest Authentication.

        Args:
            identifier (str): the identifier

        Raises:
            ValueError: if identifier is not passed

        Returns:
            Session: the connected session
        """
        if not identifier:
            raise ValueError('identifier is required')
        self.application.identifier = identifier
        self.application.authentication = GuestAuthentication()
        return await self.connect_async()

    async def connect_with_password_async(
        self,
        identifier: str,
        password: str,
        presence: Dict[str, str] = None
    ) -> Session:
        """Connect using Plain Authentication.

        Args:
            identifier (str): the identifier
            password (str): the password
            presence (Dict[str, str]): presence to be sent.

        Raises:
            ValueError: if identifier or password is not passed

        Returns:
            Session: the connected session
        """
        if not identifier:
            raise ValueError('identifier is required')
        if not password:
            raise ValueError('password is required')

        self.application.identifier = identifier
        self.application.authentication = PlainAuthentication(password)

        if presence:
            self.application.presence = presence
        return await self.connect_async()

    async def connect_with_key_async(
        self,
        identifier: str,
        key: str,
        presence: Dict[str, str] = None
    ) -> Session:
        """Connect using Key Authentication.

        Args:
            identifier (str): the identifier
            key (str): the key
            presence (Dict[str, str]): presence to be sent.

        Raises:
            ValueError: if identifier or key is not passed

        Returns:
            Session: the connected session
        """
        if not identifier:
            raise ValueError('identifier is required')
        if not key:
            raise ValueError('key is required')

        self.application.identifier = identifier
        self.application.authentication = KeyAuthentication(key)

        if presence:
            self.application.presence = presence
        return await self.connect_async()

    async def connect_async(self) -> Session:
        """Open a connection on transport and start application.

        Raises:
            ConnectionError: connection tries exceeded.

        Returns:
            Session: The connected Session
        """
        if self.__connection_try_count >= MAX_CONNECTION_TRY_COUNT:
            raise ConnectionError(
                f'Could not connect: Max connection try count of \
                {MAX_CONNECTION_TRY_COUNT} reached. Please check you network \
                and refresh the page.')

        self.__connection_try_count += 1
        self.__closing = False

        await self.transport.open_async(self.uri)
        session = await self.client_channel.establish_session_async(
            self.application.compression,
            self.application.encryption,
            f'{self.application.identifier}@{self.application.domain}',
            self.application.authentication,
            self.application.instance
        )
        await self.__send_presence_command_async()
        await self.__send_receipts_command_async()

        self.listening = True
        self.__connection_try_count = 0

        return session

    async def close_async(self) -> Session:
        """Close the open connection.

        Returns:
            Session: the closed session
        """
        self.__closing = True

        if self.client_channel.state == SessionState.ESTABLISHED:
            return await self.client_channel.send_finishing_session_async()

        if self.session_future.done():
            return self.session_future.result()
        return await self.session_future

    def connect(self) -> Session:
        """Open a connection on transport and start application.

        Raises:
            ConnectionError: connection tries exceeded.

        Returns:
            Session: The connected Session
        """  # noqa: DAR402
        loop = get_event_loop()
        return loop.run_until_complete(self.connect_async())

    def close(self) -> Session:
        """Close the open connection.

        Returns:
            Session: the closed session
        """
        loop = get_event_loop()
        return loop.run_until_complete(self.close_async())

    def send_message(self, message: Message) -> None:
        """Send a Message.

        Args:
            message (Message): Message to be sent
        """
        self.client_channel.send_message(message)

    def send_notification(self, notification: Notification) -> None:
        """Send a Notification.

        Args:
            notification (Notification): Notification to be sent
        """
        self.client_channel.send_notification(notification)

    def send_command(self, command: Command) -> None:
        """Send a command.

        Args:
            command (Command): Command to be sent
        """
        self.client_channel.send_command(command)

    async def process_command_async(
        self,
        command: Command,
        timeout: float = None
    ) -> Command:
        """Process a Command asynchronously and return the result.

        Args:
            command (Command): The Command to be processed
            timeout (float): Timeout to process the Command

        Returns:
            Command: The result Command
        """
        timeout = timeout if timeout else self.application.command_timeout
        return await self.client_channel.process_command_async(
            command,
            timeout
        )

    def process_command(
        self,
        command: Command,
        timeout: float = None
    ) -> Command:
        """Process a Command and return the result.

        Args:
            command (Command): The Command to be processed
            timeout (float): Timeout to process the Command

        Returns:
            Command: The result Command
        """
        loop = get_event_loop()
        return loop.run_until_complete(
            self.process_command_async(command, timeout)
        )

    def add_message_receiver(self, receiver: Receiver) -> Callable[[], None]:
        """Add a message receiver.

        Args:
            receiver (Receiver): the Receiver

        Returns:
            Callable[[], None]: a method to remove the receiver
        """
        return self.__add_receiver(self.__message_receivers, receiver)

    def clear_message_receivers(self) -> None:
        """Remove all message receivers."""
        self.__message_receivers = []

    def add_command_receiver(self, receiver: Receiver) -> Callable[[], None]:
        """Add a command receiver.

        Args:
            receiver (Receiver): the Receiver

        Returns:
            Callable[[], None]: a method to remove the receiver
        """
        return self.__add_receiver(self.__command_receivers, receiver)

    def clear_command_receivers(self) -> None:
        """Remove all command receivers."""
        self.__command_receivers = []

    def add_notification_receiver(
        self,
        receiver: Receiver
    ) -> Callable[[], None]:
        """Add a notification receiver.

        Args:
            receiver (Receiver): the Receiver

        Returns:
            Callable[[], None]: a method to remove the receiver
        """
        return self.__add_receiver(self.__notification_receivers, receiver)

    def clear_notification_receivers(self) -> None:
        """Remove all notification receivers."""
        self.__notification_receivers = []

    def add_session_finished_handler(
        self,
        handler: Callable[[Session], None]
    ) -> Callable[[], None]:
        """Add a session finished handler.

        Args:
            handler (Callable[[Session], None]): the handler callback

        Returns:
            Callable[[], None]: a method to remove the handler
        """
        return self.__add_handler(self.__session_finished_handlers, handler)

    def clear_session_finished_handlers(self) -> None:
        """Remove all session finished handlers."""
        self.__session_finished_handlers = []

    def add_session_failed_handler(
        self,
        handler: Callable[[Session], None]
    ) -> Callable[[], None]:
        """Add a session failed handler.

        Args:
            handler (Callable[[Session], None]): the handler callback

        Returns:
            Callable[[], None]: a method to remove the handler
        """
        return self.__add_handler(self.__session_failed_handlers, handler)

    def clear_session_failed_handlers(self) -> None:
        """Remove all session failed handlers."""
        self.__session_failed_handlers = []

    def on_listening_changed(self, value: bool) -> None:
        """Handle callback to client listening changes.

        This method can be overwrited.

        Args:
            value (bool): the new listening value
        """
        pass

    def __initialize_client_channel(self) -> None:
        """Initialize client channel listeners."""
        self.transport.on_close = self.__transport_on_close

        self.session_future = Future()

        self.client_channel = ClientChannel(self.transport, True, False)
        self.client_channel.on_message = self.__client_channel_on_message
        self.client_channel.on_notification = self.__client_channel_on_notification  # noqa: E501
        self.client_channel.on_command = self.__client_channel_on_command
        self.client_channel.on_session_finished = self.__client_channel_on_session_finished  # noqa: E501
        self.client_channel.on_session_failed = self.__client_channel_on_session_failed  # noqa: E501

    def __add_handler(
        self,
        handler_list: List[Callable[[Session], None]],
        handler: Callable[[Session], None]
    ) -> Callable[[], None]:
        handler_list.append(handler)
        position = len(handler_list) - 1
        return lambda: handler_list.pop(position)

    def __add_receiver(
        self,
        receiver_list: List[Receiver],
        receiver: Receiver
    ) -> Callable[[], None]:
        receiver_list.append(receiver)
        return lambda: receiver_list.remove(receiver)

    async def __send_presence_command_async(self) -> Command:
        if isinstance(self.application.authentication, GuestAuthentication):
            return None

        command = Command(
            CommandMethod.SET,
            '/presence',
            'application/vnd.lime.presence+json',
            self.application.presence
        )
        return await self.process_command_async(command)

    async def __send_receipts_command_async(self) -> Command:
        if isinstance(self.application.authentication, GuestAuthentication):
            return None

        command = Command(
            CommandMethod.SET,
            '/receipt',
            'application/vnd.lime.receipt+json',
            {
                'events': [
                    NotificationEvent.FAILED,
                    NotificationEvent.ACCEPTED,
                    NotificationEvent.DISPATCHED,
                    NotificationEvent.RECEIVED,
                    NotificationEvent.CONSUMED
                ]
            }
        )
        return await self.process_command_async(command)

    def __client_channel_on_session_finished(self, session: Session) -> None:
        self.session_future.set_result(session)
        self.__notify_handlers(self.__session_finished_handlers, session)

    def __client_channel_on_session_failed(self, session: Session) -> None:
        self.session_future.set_exception(session)
        self.__notify_handlers(self.__session_failed_handlers, session)

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
        resolve = self.__command_resolves.get(command.id)
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
            self.client_channel.local_node.lower().startswith(
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

        try:
            self.__notify_message_receivers(message)
            self.__notify(should_notify, message)
        except Exception as error:
            self.__notify(should_notify, message, error)

    def __transport_on_close(self) -> None:
        self.listening = False
        if not self.__closing:
            # Use an exponential backoff for the timeout in seconds
            timeout = (100 * (2 ** self.__connection_try_count)) / 1000.0

            # Try to reconnect after the timeout
            sleep(timeout)
            if not self.__closing:
                self.transport = self.__transport_factory()
                self.__initialize_client_channel()
                ensure_future(self.connect_async())

    def __notify_message_receivers(self, message: Message) -> None:
        for receiver in self.__message_receivers:
            result: bool = None
            if receiver.predicate(message):
                result = receiver.callback(message)
            if result is False:
                raise ValueError

    def __notify(
        self,
        should_notify: bool,
        message: Message,
        error: Exception = None
    ) -> None:
        if not should_notify:
            return

        if error:
            notification = Notification(
                NotificationEvent.FAILED,
                Reason(
                    ReasonCode.APPLICATION_ERROR,
                    str(error)
                )
            )
            notification.id = message.id
            notification.from_n = message.from_n
            self.send_notification(notification)

        if self.application.notify_consumed:
            notification = Notification(NotificationEvent.CONSUMED)
            notification.id = message.id
            notification.to = message.pp if message.pp else message.from_n
            notification.metadata = {
                '#message.to': message.to
            }
            self.send_notification(notification)

    def __get_extension(self, type: Type, to: str = None) -> ExtensionBase:
        extension = self.__extensions.get(type)
        if not extension:
            extension = type(self, to)
            self.__extensions[type] = extension
        return extension

    def __reflect(self, any: Any) -> Any:
        return any
