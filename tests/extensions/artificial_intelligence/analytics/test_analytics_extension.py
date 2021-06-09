from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import AnalyticsExtension
from ....async_mock import async_return

AI_TO = 'postmaster@ai.msging.net'


class TestAnalyticsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> AnalyticsExtension:
        yield AnalyticsExtension(mocker.MagicMock(), 'msging.net')

    @mark.asyncio
    async def test_get_analysis_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
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
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        analysis_resource = {
            'text': 'Test'
        }
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock
        expected_command = Command(
            'set',
            '/analysis',
            'application/vnd.iris.ai.analysis-request+json',
            analysis_resource
        )
        expected_command.to = AI_TO

        # Act
        await target.analyse_async(analysis_resource)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analysis_by_email_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
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
        await target.set_analysis_by_email_async(email, filter)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analysis_feedback_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        analysis_feedback = [
            {
                'IntentionId': '1234',
                'AnalysisId': '4321'
            }
        ]
        analysis_feedback_resource = {
            'itemType': 'application/vnd.iris.ai.analysis-feedback+json',
            'items': analysis_feedback
        }
        expected_command = Command(
            'set',
            '/analysis/feedback',
            'application/vnd.lime.collection+json',
            analysis_feedback_resource
        )
        expected_command.to = AI_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_analyses_feedback_async('1234', analysis_feedback)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analyses_feedback_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        analysis_feedback = {
            'IntentionId': '1234',
            'AnalysisId': '4321'
        }

        expected_command = Command(
            'set',
            '/analysis/feedback',
            'application/vnd.iris.ai.analysis-feedback+json',
            analysis_feedback
        )
        expected_command.to = AI_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_analysis_feedback_async('1234', analysis_feedback)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_analytics_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
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
        await target.get_analytics_async(analytics_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_analytics_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
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
        await target.set_analytics_async(resource)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_analytics_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
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
        await target.delete_analytics_async(analytics_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
