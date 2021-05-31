from typing import Awaitable
from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import MediaExtension
from ...utilities import async_return

MEDIA_TO = 'postmaster@media.mging.net'


class TestMediaExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> MediaExtension:
        yield MediaExtension(mocker.MagicMock(), 'mging.net')

    @mark.parametrize('secure', [True, False, None])
    @mark.asyncio
    async def test_get_upload_token_async(
        self,
        mocker: MockerFixture,
        target: MediaExtension,
        secure: bool
    ) -> Awaitable:
        # Arrange
        uri = f'/upload-media-uri?secure={secure}' if secure is not None else '/upload-media-uri'  # noqa: E501
        expected_command = Command('get', uri)
        expected_command.to = MEDIA_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_upload_token_async(secure)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_refresh_media(
        self,
        mocker: MockerFixture,
        target: MediaExtension
    ) -> Awaitable:
        # Arrange
        media = 'my-id'
        expected_command = Command(
            'get', f'/refresh-media-uri/{media}?foo=bar'
        )
        expected_command.to = MEDIA_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.refresh_media_async(media, foo='bar')

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
