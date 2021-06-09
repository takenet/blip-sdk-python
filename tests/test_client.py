from typing import Callable
from lime_python import (Command, CommandMethod, CommandStatus,
                         GuestAuthentication, KeyAuthentication, Message,
                         Notification, NotificationEvent, PlainAuthentication,
                         Session, SessionState)
from pytest import fixture, mark, raises
from pytest_mock import MockerFixture

from src import Application, ChatExtension, Client, MediaExtension
from src.blip_sdk_python.receiver import Receiver

from .async_mock import async_return

ESTABLISHED_SESSION = Session(SessionState.ESTABLISHED)
FINISHED_SESSION = Session(SessionState.FINISHED)


class TestClient:

    @fixture
    def target(self, mocker: MockerFixture) -> Client:
        yield Client('127.0.0.1:8124', mocker.MagicMock(), Application())

    def test_get_chat_extension(self, target: Client) -> None:
        # Act
        result = target.chat_extension
        result2 = target.chat_extension

        # Assert
        assert isinstance(result, ChatExtension)
        assert result == result2

    def test_get_media_extension(self, target: Client) -> None:
        # Act
        result = target.media_extension
        result2 = target.media_extension

        # Assert
        assert isinstance(result, MediaExtension)
        assert result == result2

    @mark.asyncio
    async def test_connect_with_guest_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        identifier = 'testidentity'

        connect_mock = mocker.MagicMock(
            return_value=async_return(ESTABLISHED_SESSION)
        )
        target.connect_async = connect_mock

        # Act
        result = await target.connect_with_guest_async(identifier)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            GuestAuthentication
        )
        assert result == ESTABLISHED_SESSION

        connect_mock.assert_called_once()

    @mark.asyncio
    async def test_connect_with_guest_failed_async(
        self,
        target: Client
    ) -> None:
        # Act/Assert
        with raises(ValueError):
            await target.connect_with_guest_async(None)

    @mark.asyncio
    async def test_connect_with_password_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        identifier = 'testidentity'
        password = 'psswd'

        connect_mock = mocker.MagicMock(
            return_value=async_return(ESTABLISHED_SESSION)
        )
        target.connect_async = connect_mock

        # Act
        result = await target.connect_with_password_async(identifier, password)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            PlainAuthentication
        )
        assert result == ESTABLISHED_SESSION

        connect_mock.assert_called_once()

    @mark.asyncio
    async def test_connect_with_password_failed_async(
        self,
        target: Client
    ) -> None:
        # Act/Assert
        with raises(ValueError):
            await target.connect_with_password_async(None, None)

    @mark.asyncio
    async def test_connect_with_key_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        identifier = 'testidentity'
        key = 'Key asdad=='

        connect_mock = mocker.MagicMock(
            return_value=async_return(ESTABLISHED_SESSION)
        )
        target.connect_async = connect_mock

        # Act
        result = await target.connect_with_key_async(identifier, key)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            KeyAuthentication
        )
        assert result == ESTABLISHED_SESSION

        connect_mock.assert_called_once()

    @mark.asyncio
    async def test_connect_with_key_failed_async(
        self,
        target: Client
    ) -> None:
        # Act/Assert
        with raises(ValueError):
            await target.connect_with_key_async(None, None)

    @mark.asyncio
    async def test_connect_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        open_mock = mocker.MagicMock(return_value=async_return(None))
        target.transport.open_async = open_mock

        session_mock = mocker.MagicMock(
            return_value=async_return(ESTABLISHED_SESSION)
        )
        target.client_channel.establish_session_async = session_mock

        command_mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.process_command_async = command_mock
        target.application.authentication = KeyAuthentication('key')

        # Act
        result = await target.connect_async()

        # Assert
        assert result == ESTABLISHED_SESSION

        open_mock.assert_called_once_with(target.uri)

        session_mock.assert_called_once_with(
            target.application.compression,
            target.application.encryption,
            f'{target.application.identifier}@{target.application.domain}',
            target.application.authentication,
            target.application.instance
        )

        command_mock.assert_any_call(
            Command(
                CommandMethod.SET,
                '/presence',
                'application/vnd.lime.presence+json',
                target.application.presence
            )
        )
        command_mock.assert_any_call(
            Command(
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
        )

    @mark.asyncio
    async def test_connect_guest_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        open_mock = mocker.MagicMock(return_value=async_return(None))
        target.transport.open_async = open_mock

        session_mock = mocker.MagicMock(
            return_value=async_return(ESTABLISHED_SESSION)
        )
        target.client_channel.establish_session_async = session_mock

        command_mock = mocker.MagicMock(return_value=None)
        target.client_channel.send_command = command_mock

        # Act
        result = await target.connect_async()

        # Assert
        assert result == ESTABLISHED_SESSION

        open_mock.assert_called_once_with(target.uri)

        session_mock.assert_called_once_with(
            target.application.compression,
            target.application.encryption,
            f'{target.application.identifier}@{target.application.domain}',
            target.application.authentication,
            target.application.instance
        )

        # Guest auth shouldn't send receipts and presence
        command_mock.assert_not_called()

    @mark.asyncio
    async def test_close_open_connection_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        target.client_channel.state = SessionState.ESTABLISHED

        session_mock = mocker.MagicMock(
            return_value=async_return(FINISHED_SESSION)
        )
        target.client_channel.send_finishing_session_async = session_mock

        # Act
        result = await target.close_async()

        # Assert
        assert result == FINISHED_SESSION
        session_mock.assert_called_once()

    @mark.asyncio
    async def test_close_closed_connection_async(
        self,
        target: Client
    ) -> None:
        # Arrange
        target.session_future.set_result(FINISHED_SESSION)

        # Act
        result = await target.close_async()

        # Assert
        assert result == FINISHED_SESSION

    def test_send_message(self, target: Client, mocker: MockerFixture) -> None:
        # Arrange
        message = Message('text/plain', 'foo')

        send_mock = mocker.MagicMock()
        target.client_channel.send_message = send_mock

        # Act
        target.send_message(message)

        # Assert
        send_mock.assert_called_once_with(message)

    def test_send_notification(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        notification = Notification(NotificationEvent.ACCEPTED)

        send_mock = mocker.MagicMock()
        target.client_channel.send_notification = send_mock

        # Act
        target.send_notification(notification)

        # Assert
        send_mock.assert_called_once_with(notification)

    def test_send_command(self, target: Client, mocker: MockerFixture) -> None:
        # Arrange
        command = Command(CommandMethod.GET, '/ping')

        send_mock = mocker.MagicMock()
        target.client_channel.send_command = send_mock

        # Act
        target.send_command(command)

        # Assert
        send_mock.assert_called_once_with(command)

    @mark.asyncio
    async def test_process_command_async(
        self,
        target: Client,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        command = Command(CommandMethod.GET, '/ping')
        command_res = Command(
            CommandMethod.GET,
            resource={},
            status=CommandStatus.SUCCESS
        )

        send_mock = mocker.MagicMock(return_value=async_return(command_res))
        target.client_channel.process_command_async = send_mock

        # Act
        result = await target.process_command_async(command)

        # Assert
        assert result == command_res
        send_mock.assert_called_once_with(
            command,
            target.application.command_timeout
        )

    def test_add_message_receiver(self, target: Client) -> None:
        # Arrange
        rec = Receiver(True, lambda env: env)

        # Act
        remove_rec = target.add_message_receiver(rec)

        # Assert
        assert isinstance(remove_rec, Callable)

    def test_add_command_receiver(self, target: Client) -> None:
        # Arrange
        rec = Receiver(True, lambda env: env)

        # Act
        remove_rec = target.add_command_receiver(rec)

        # Assert
        assert isinstance(remove_rec, Callable)

    def test_add_notification_receiver(self, target: Client) -> None:
        # Arrange
        rec = Receiver(True, lambda env: env)

        # Act
        remove_rec = target.add_notification_receiver(rec)

        # Assert
        assert isinstance(remove_rec, Callable)

    def test_add_session_finished_handler(self, target: Client) -> None:
        # Arrange
        handler = lambda session: session

        # Act
        remove_handler = target.add_session_finished_handler(handler)

        # Assert
        assert isinstance(remove_handler, Callable)

    def test_add_session_failed_handler(self, target: Client) -> None:
        # Arrange
        handler = lambda session: session

        # Act
        remove_handler = target.add_session_failed_handler(handler)

        # Assert
        assert isinstance(remove_handler, Callable)
