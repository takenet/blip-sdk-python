from typing import Awaitable
from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import MediaExtension
from ...utilities import async_return


class TestMediaExtension:

    @fixture(autouse=True)
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
        command_id = 'some-id'
        expected_result = Command.from_json(
            {
                'type': 'text/plain',
                'resource': 'https://media.msging.net/media/media-id',
                'method': 'get',
                'status': 'success',
                'id': command_id
            }
        )

        target.client.process_command_async = mocker.MagicMock(
            return_value=async_return(expected_result)
        )

        # Act
        result = await target.get_upload_token_async(secure)

        # Assert
        assert result == expected_result

    @mark.asyncio
    async def test_refresh_media(
        self,
        mocker: MockerFixture,
        target: MediaExtension
    ) -> Awaitable:
        # Arrange
        media = 'media-id'
        expected_result = Command.from_json(
            {
                'type': 'text/plain',
                'resource': f'https://my-media/{media}',
                'method': 'get',
                'status': 'success',
                'id': 'eef6e5c4-3a06-4baa-aca1-a7a8fd2ce58b'
            }
        )

        target.client.process_command_async = mocker.MagicMock(
            return_value=async_return(expected_result)
        )

        # Act
        result = await target.refresh_media_async(media)

        # Assert
        assert result == expected_result
