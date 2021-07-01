from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import AIExtension
from ....async_mock import async_return

AI_TO = 'postmaster@ai.msging.net'


class TestAIAnalyticsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> AIExtension:
        yield AIExtension(mocker.MagicMock(), 'msging.net')

    @mark.asyncio
    async def test_get_analysis_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        uri = '/analysis?$skip=0&$take=100&$ascending=True'
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock
        expected_command = Command(
            'get',
            uri
        )

        expected_command.to = AI_TO
        # Act
        await target.get_analysis_async(0, 100, True)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_analyse_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock
        expected_command = Command(
            'set',
            '/analysis',
            'application/vnd.iris.ai.analysis-request+json',
            {'text': 'input'}
        )
        expected_command.to = AI_TO

        # Act
        await target.analyse_async('input')

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_send_analysis_by_email_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        email = 'test@take.net'
        filter = "requestDateTime ge datetimeoffset'2019-04-29T16:31:00.000Z' and requestDateTime le datetimeoffset'2019-05-30T16:31:00.000Z'"  # noqa: E501
        analysis_by_email_resource = {
            'email': email,
            'filter': "/analysis?$filter=requestDateTime%20ge%20datetimeoffset'2019-04-29T16%3A31%3A00.000Z'%20and%20requestDateTime%20le%20datetimeoffset'2019-05-30T16%3A31%3A00.000Z'"  # noqa: E501, WPS323
        }

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock
        expected_command = Command(
            'set',
            '/enhancement/send-by-email',
            'application/json',
            analysis_by_email_resource
        )
        expected_command.to = AI_TO

        # Act
        await target.send_analysis_by_email_async(email, filter)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analysis_feedback_no_feedback_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        intention_id = '1234'
        analysis_id = '4321'

        resource = {
            'intentionId': intention_id,
            'analysisId': analysis_id
        }
        expected_command = Command(
            'set',
            '/analysis/feedback',
            'application/vnd.iris.ai.analysis-feedback+json',
            resource,
            to=AI_TO
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_analysis_feedback_async(analysis_id, intention_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analysis_feedback_no_intention_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        feedback = 'approved'
        analysis_id = '4321'

        resource = {
            'feedback': feedback
        }
        expected_command = Command(
            'set',
            f'/analysis/{analysis_id}/feedback',
            'application/vnd.iris.ai.analysis-feedback+json',
            resource,
            to=AI_TO
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_analysis_feedback_async(
            analysis_id,
            feedback=feedback
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analysis_feedback_complete_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        analysis_id = '1234'
        intent_id = '4321'
        feedback = 'rejected'

        resource = {
            'feedback': feedback,
            'intentionId': intent_id
        }
        expected_command = Command(
            'set',
            f'/analysis/{analysis_id}/feedback',
            'application/vnd.iris.ai.analysis-feedback+json',
            resource,
            to=AI_TO
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_analysis_feedback_async(
            analysis_id,
            intent_id,
            feedback
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_confusion_matrix_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        analytics_id = '1234'
        expected_command = Command(
            'get',
            f'/analytics/confusion-matrix/{analytics_id}'
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_confusion_matrix_async(analytics_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_confusion_matrix_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        resource = {
            'version': 'teste',
            'sampleSize': 2
        }
        expected_command = Command(
            'set',
            '/analytics/confusion-matrix',
            'application/vnd.iris.ai.confusion-matrix+json',
            resource
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_confusion_matrix_async(resource)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_confusion_matrix_async(
        self,
        mocker: MockerFixture,
        target: AIExtension
    ) -> None:
        # Arrange
        analytics_id = '1234'
        expected_command = Command(
            'delete',
            f'/analytics/confusion-matrix/{analytics_id}'
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_confusion_matrix_async(analytics_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
