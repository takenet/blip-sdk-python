from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import ContentAssistantExtension
from ....utilities import async_return


class TestContentAssistantExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> ContentAssistantExtension:
        yield ContentAssistantExtension(mocker.MagicMock())

    @mark.asyncio
    async def test_analyse_content(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:
        # Arrange

        analysis_object = {
            'intent': 'intent',
            'entities': ['entity'],
            'minEntityMatch': 1
        }
        expected_command = Command(
            'set',
            '/content/analysis',
            'application/vnd.iris.ai.analysis-request+json',
            analysis_object
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.analyse_content(analysis_object)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_match_content(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:

        combinations_object = [{
            'intent': 'intent',
            'entities': ['entity'],
            'minEntityMatch': 1
        }]

        expected_command = Command(
            'set',
            '/content/analysis',
            'application/vnd.iris.ai.content-combination+json',
            combinations_object
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.match_content(combinations_object)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_contents(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:
        uri = '/content?$skip=0&$take=100&$ascending=False'

        expected_command = Command('get', uri)

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_contents(0, 100)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_content(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:

        content_id = '1234'

        expected_command = Command(
            'get',
            f'/content/{content_id}'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_content(content_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_content_result(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:

        # Arrange
        content_id = '1234'
        content_result_object = {
            'id': content_id,
            'name': 'content_name',
            'result': {
                'type': 'text/plain',
                'content': 'description'
            },
            'combinations': [
                {
                    'intent': 'intent',
                    'entities': ['entity'],
                    'minEntityMatch': 1,
                    'intentName': 'intent'
                }
            ]
        }

        expected_command = Command(
            'set',
            '/content/1234',
            'application/vnd.iris.ai.content-result+json',
            content_result_object
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_content_result(content_id, content_result_object)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_content_combination(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:
        # Arrange
        content_id = '1234'
        content_combination_object = {
            'intent': 'intent',
            'entities': ['entity'],
            'minEntityMatch': 1,
            'intentName': 'intent'
        }

        expected_command = Command(
            'set',
            f'/content/{content_id}',
            'application/vnd.iris.ai.content-combination+json',
            content_combination_object
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_content_combination(
            content_id,
            content_combination_object
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_content_combinations(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:
        # Arrange
        content_id = '1234'
        combinations = [
            {
                'intent': 'intent',
                'entities': ['entity'],
                'minEntityMatch': 1,
                'intentName': 'intent'
            }
        ]
        content_combinations = {
            'itemType': 'application/vnd.iris.ai.content-combination+json',
            'items': combinations
        }

        expected_command = Command(
            'set',
            f'/content/{content_id}',
            'application/vnd.lime.collection+json',
            content_combinations
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_content_combinations(content_id, combinations)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_content(
        self,
        mocker: MockerFixture,
        target: ContentAssistantExtension
    ) -> None:

        content_id = '1234'

        expected_command = Command(
            'delete',
            f'/content/{content_id}'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_content(content_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
