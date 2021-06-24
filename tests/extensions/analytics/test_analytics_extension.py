from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import AnalyticsExtension
from ...async_mock import async_return

ANALYTICS_TO = 'postmaster@analytics.msging.net'


class TestAnalyticsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> AnalyticsExtension:
        yield AnalyticsExtension(mocker.MagicMock(), 'msging.net')

    @mark.asyncio
    async def test_get_events_track_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        expected_command = Command(
            'get',
            '/event-track'
        )

        expected_command.to = ANALYTICS_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_categories_async()

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_event_track_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        category = 'Saudacao Inicial'
        start_date = '2020-12-17'
        end_date = '2021-12-17'
        expected_command = Command(
            'get',
            '/event-track/Saudacao%20Inicial?startDate=2020-12-17&endDate=2021-12-17&$take=10'  # noqa: E501
        )

        expected_command.to = ANALYTICS_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_category_actions_counter_async(
            category,
            start_date,
            end_date,
            10
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_create_event_track_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Assert
        category = 'payments'
        action = 'success-order'
        identity = '123456@messenger.gw.msging.net'
        extras = {
            'nome': 'Teste'
        }

        expected_command = Command(
            'set',
            '/event-track',
            'application/vnd.iris.eventTrack+json',
            {
                'category': category,
                'action': action,
                'contact': {
                    'identity': identity
                },
                'extras': extras
            }
        )

        expected_command.to = ANALYTICS_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.create_event_track_async(
            category,
            action,
            identity,
            extras
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_event_track_details_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Assert
        category = 'Saudacao Inicial'
        action = 'Contador'
        start_date = '2020-12-17'
        end_date = '2021-12-17'
        expected_command = Command(
            'get',
            '/event-track/Saudacao%20Inicial/Contador?startDate=2020-12-17&endDate=2021-12-17&$take=10'  # noqa: E501
        )
        expected_command.to = ANALYTICS_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.get_event_details_async(
            category,
            action,
            start_date,
            end_date,
            10
        )
        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_event_track_async(
        self,
        mocker: MockerFixture,
        target: AnalyticsExtension
    ) -> None:
        # Arrange
        category = 'Saudacao Inicial'
        expected_command = Command(
            'delete',
            '/event-track/Saudacao%20Inicial'
        )

        expected_command.to = ANALYTICS_TO

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_category_async(category)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
