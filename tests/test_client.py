from lime_python import (Command, CommandMethod, GuestAuthentication,
                         KeyAuthentication, NotificationEvent,
                         PlainAuthentication, Session, SessionState)
from lime_transport_websocket import WebSocketTransport
from pytest import fixture, mark, raises
from pytest_mock import MockerFixture

from src import Application, ChatExtension, Client, MediaExtension

from .async_mock import async_return


class TestClient:

    @fixture
    def target(self) -> Client:
        yield Client('127.0.0.1:8124', WebSocketTransport(), Application())

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

        open_mock = mocker.MagicMock(return_value=async_return(None))
        target.transport.open_async = open_mock

        session_mock = mocker.MagicMock(
            return_value=async_return(Session(SessionState.ESTABLISHED))
        )
        target.client_channel.establish_session_async = session_mock

        command_mock = mocker.MagicMock(return_value=None)
        target.client_channel.send_command = command_mock

        # Act
        result = await target.connect_with_guest_async(identifier)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            GuestAuthentication
        )
        assert result == Session(SessionState.ESTABLISHED)

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

        open_mock = mocker.MagicMock(return_value=async_return(None))
        target.transport.open_async = open_mock

        session_mock = mocker.MagicMock(
            return_value=async_return(Session(SessionState.ESTABLISHED))
        )
        target.client_channel.establish_session_async = session_mock

        command_mock = mocker.MagicMock(return_value=None)
        target.client_channel.send_command = command_mock

        # Act
        result = await target.connect_with_password_async(identifier, password)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            PlainAuthentication
        )
        assert result == Session(SessionState.ESTABLISHED)

        open_mock.assert_called_once_with(target.uri)

        session_mock.assert_called_once_with(
            target.application.compression,
            target.application.encryption,
            f'{target.application.identifier}@{target.application.domain}',
            target.application.authentication,
            target.application.instance
        )

        # Guest auth shouldn't send receipts and presence
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

        open_mock = mocker.MagicMock(return_value=async_return(None))
        target.transport.open_async = open_mock

        session_mock = mocker.MagicMock(
            return_value=async_return(Session(SessionState.ESTABLISHED))
        )
        target.client_channel.establish_session_async = session_mock

        command_mock = mocker.MagicMock(return_value=None)
        target.client_channel.send_command = command_mock

        # Act
        result = await target.connect_with_key_async(identifier, key)

        # Assert
        assert target.application.identifier == identifier
        assert isinstance(
            target.application.authentication,
            KeyAuthentication
        )
        assert result == Session(SessionState.ESTABLISHED)

        open_mock.assert_called_once_with(target.uri)

        session_mock.assert_called_once_with(
            target.application.compression,
            target.application.encryption,
            f'{target.application.identifier}@{target.application.domain}',
            target.application.authentication,
            target.application.instance
        )

        # Guest auth shouldn't send receipts and presence
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
    async def test_connect_with_key_failed_async(
        self,
        target: Client
    ) -> None:
        # Act/Assert
        with raises(ValueError):
            await target.connect_with_key_async(None, None)
