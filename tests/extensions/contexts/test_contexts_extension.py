from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import ContextsExtension
from ...async_mock import async_return


class TestContextsExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> ContextsExtension:
        yield ContextsExtension(mocker.MagicMock())

    @mark.asyncio
    async def test_get_bots_contexts_async(
        self,
        mocker: MockerFixture,
        target: ContextsExtension
    ) -> None:
        # Arrange
        expected_command = Command('get', '/contexts?$skip=0&$take=100')

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_bot_contexts_async(0, 100)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_context_variables_async(
        self,
        mocker: MockerFixture,
        target: ContextsExtension
    ) -> None:
        # Arrange
        user_id = '12345@wa.gw.msging.net'
        expected_user_id = '12345%40wa.gw.msging.net'
        expected_command = Command(
            'get',
            f'/contexts/{expected_user_id}?$skip=0&$take=100' +
            '&withContextValue=False'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_context_variables(user_id, 0, 100)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_get_context_variable_async(
        self,
        mocker: MockerFixture,
        target: ContextsExtension
    ) -> None:
        # Arrange
        user_id = '12345@wa.gw.msging.net'
        expected_user_id = '12345%40wa.gw.msging.net'
        variable_name = 'attendanceTime'
        expected_command = Command(
            'get',
            f'/contexts/{expected_user_id}/{variable_name}'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.get_context_variable(user_id, variable_name)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_context_variable_async(
        self,
        mocker: MockerFixture,
        target: ContextsExtension
    ) -> None:
        # Arrange
        user_id = '12345@wa.gw.msging.net'
        expected_user_id = '12345%40wa.gw.msging.net'
        variable_name = 'isAttendanceTime'
        expected_command = Command(
            'set',
            f'/contexts/{expected_user_id}/{variable_name}',
            type_n='text/plain',
            resource='true'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.set_context_variable(
            user_id,
            variable_name,
            'text/plain',
            'true'
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_context_variable_async(
        self,
        mocker: MockerFixture,
        target: ContextsExtension
    ) -> None:
        # Arrange
        user_id = '12345@wa.gw.msging.net'
        expected_user_id = '12345%40wa.gw.msging.net'
        variable_name = 'isAttendanceTime'
        expected_command = Command(
            'delete',
            f'/contexts/{expected_user_id}/{variable_name}'
        )

        mock = mocker.MagicMock(
            return_value=async_return(None)
        )
        target.client.process_command_async = mock

        # Act
        await target.delete_context_variable_async(
            user_id,
            variable_name
        )

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
