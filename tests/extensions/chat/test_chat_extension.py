from typing import Awaitable
from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import ChatExtension
from ...utilities import async_return


class TestChatExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> ChatExtension:
        yield ChatExtension(mocker.MagicMock())

    @mark.asyncio
    async def test_get_threads_async(
        self,
        mocker: MockerFixture,
        target: ChatExtension
    ) -> Awaitable:
        # Arrange
        expected_command = Command('get', '/threads?foo=bar')

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_threads_async(foo='bar')

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_thread_async(
        self,
        mocker: MockerFixture,
        target: ChatExtension
    ) -> Awaitable:
        # Arrange
        expected_command = Command(
            'get', '/threads/my-id?refreshExpiredMedia=True'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_thread_async('my-id', refresh_expired_media=True)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_thread_unread_messages_async(
        self,
        mocker: MockerFixture,
        target: ChatExtension
    ) -> Awaitable:
        # Arrange
        expected_command = Command(
            'get', '/threads/my-id/unread'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_thread_unread_messages_async('my-id')

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_thread_async(
        self,
        mocker: MockerFixture,
        target: ChatExtension
    ) -> Awaitable:
        # Arrange
        expected_command = Command(
            'set',
            '/threads/my-id',
            'application/vnd.iris.thread-message+json',
            {}
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_thread_async('my-id', {})

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
