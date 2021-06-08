from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import AnalyticsExtension
from ....utilities import async_return


class TestAnalyticsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> AnalyticsExtension:
        yield AnalyticsExtension(mocker.MagicMock())

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
        filter = "requestDateTime ge datetimeoffset 2019-04-29T16:31:00.000Z and requestDateTime le datetimeoffset 2019-05-30T16:31:00.000Z"  # noqa E501
        analysis_by_email_resource = {
            'email': email,
            'filter': f"/analysis?$filter=requestDateTime%20ge%20datetimeoffset'2019-04-29T16%3A31%3A00.000Z'%20and%20requestDateTime%20le%20datetimeoffset'2019-05-30T16%3A31%3A00.000Z'"  # noqa E501
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

        # Act
        await target.set_analysis_by_email_async(email, filter)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
