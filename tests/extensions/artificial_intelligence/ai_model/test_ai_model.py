from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import AiModelExtension
from ....async_mock import async_return

AI_TO = 'postmaster@ai.msging.net'


class TestAiModelExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> AiModelExtension:
        yield AiModelExtension(mocker.MagicMock(), 'msging.net')

    @mark.asyncio
    async def test_get_models_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Arrange
        expected_command = Command(
            'get',
            '/models?$skip=0&$take=100&$ascending=False',
        )

        expected_command.to = AI_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_models_async(0, 100, False)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_model_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Assert
        model_id = '1234'
        expected_command = Command(
            'get',
            '/model/1234'
        )

        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.get_model_async(model_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_model_summary_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Assert
        expected_command = Command(
            'get',
            '/models/summary'
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.get_model_summary_async()

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_last_trained_or_published_model_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Assert
        expected_command = Command(
            'get',
            '/models/last-trained-or-published'
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.get_last_trained_or_published_model_async()

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_train_model_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Assert
        expected_command = Command(
            'set',
            '/models',
            'application/vnd.iris.ai.model-training+json',
            {}
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.train_model_async()

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_publish_model_async(
        self,
        mocker: MockerFixture,
        target: AiModelExtension
    ) -> None:
        # Assert
        model_id = '1234'
        command_resource = {
            'id': model_id
        }
        expected_command = Command(
            'set',
            '/models',
            'application/vnd.iris.ai.model-publishing+json',
            command_resource
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.publish_model_async(model_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
