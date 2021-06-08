from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import IntentsExtension
from ....utilities import async_return


class TestIntentsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> IntentsExtension:
        yield IntentsExtension(mocker.MagicMock())

    @mark.asyncio
    async def test_get_intent_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        intent_uri = f'/intentions/{intent_id}?deep=True'
        expected_command = Command('get', intent_uri)
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_intent_async(intent_id, True)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_intents_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_uri = '/intentions?$skip=0&$take=100&deep=True&$ascending=False'
        expected_command = Command('get', intent_uri)
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_intents_async(0, 100, True)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_intent(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_resource = {
            'name': 'intents'
        }
        expected_command = Command(
            'set',
            '/intentions',
            'application/vnd.iris.ai.intention+json',
            intent_resource
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_intent_async(intent_resource)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_intents(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intents = [
            {
                'name': 'intents'
            }
        ]
        intent_resource = {
            'itemType': 'application/vnd.iris.ai.intention+json',
            'items': intents
        }
        expected_command = Command(
            'set',
            '/intentions',
            'application/vnd.lime.collection+json',
            intent_resource
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_intents_async(intents)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_merge_intent(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent = {
            'name': 'intents'
        }
        expected_command = Command(
            'merge',
            '/intentions',
            'application/vnd.iris.ai.intention+json',
            intent
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.merge_intent_async(intent)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_merge_intents(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intents = [
            {
                'name': 'intents'
            }
        ]
        intents_resource = {
            'itemType': 'application/vnd.iris.ai.intention+json',
            'items': intents
        }
        expected_command = Command(
            'merge',
            '/intentions',
            'application/vnd.lime.collection+json',
            intents_resource
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.merge_intents_async(intents)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_intent_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        expected_command = Command(
            'delete',
            f'/intentions/{intent_id}'
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_intent_async(intent_id)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_intents_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        expected_command = Command(
            'delete',
            '/intentions'
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_intents_async()

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_intent_answers_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        expected_command = Command(
            'get',
            f'/intentions/{intent_id}/answers?$skip=0&$take=100&$ascending=False'  # noqa=E501
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_intent_answers_async(intent_id)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_intent_answers_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        answers = [
            {
                'type': 'text/plain',
                'value': 'Which flavor do you want?'
            }
        ]
        set_answer_resource = {
            'itemType': 'application/vnd.iris.ai.answer+json',
            'items': answers
        }
        expected_command = Command(
            'set',
            f'/intentions/{intent_id}/answers',
            'application/vnd.lime.collection+json',
            set_answer_resource
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_intent_answers_async(intent_id, answers)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_intent_answers_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        answer_id = '4321'
        expected_command = Command(
            'delete',
            f'/intentions/{intent_id}/answers/{answer_id}'
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_intent_answers_async(intent_id, answer_id)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_intent_questions_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        expected_command = Command(
            'get',
            f'/intentions/{intent_id}/questions'
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_intent_questions_async(intent_id)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_intent_questions_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        questions = [
            {
                'text': 'Qual a pizza',
            },
            {
                'text': 'Qual o sanduiche',
            }
        ]
        set_question_resource = {
            'itemType': 'application/vnd.iris.ai.question+json',
            'items': questions
        }
        expected_command = Command(
            'set',
            f'/intentions/{intent_id}/questions',
            'application/vnd.lime.collection+json',
            set_question_resource
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_intent_questions_async(intent_id, questions)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_intent_question_async(
        self,
        mocker: MockerFixture,
        target: IntentsExtension
    ) -> None:
        # Arrange
        intent_id = '1234'
        question_id = '4321'
        expected_command = Command(
            'delete',
            f'/intentions/{intent_id}/questions/{question_id}'
        )
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_intent_question_async(intent_id, question_id)

        # Arrange
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
