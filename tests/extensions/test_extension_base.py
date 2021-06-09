from asyncio import Future
from typing import Any
from lime_python import Command
from pytest import mark
from pytest_mock import MockerFixture
from src import ExtensionBase


class TestExtensionBase:

    def test_build_uri(self) -> None:
        # Arrange
        target = self.get_target()
        template_uri = 'https://take.net/{0}/{1}'
        expected_uri = 'https://take.net/solutions%20lab/gabriel'  # noqa: WPS323, E501

        # Act
        result = target.build_uri(
            template_uri,
            'solutions lab',
            'gabriel'
        )

        # Assert
        assert result == expected_uri

    @mark.parametrize('uri', ['https://take.net', 'https://take.net?'])
    def test_build_resource_query(self, uri: str) -> None:
        # Arrange
        target = self.get_target()
        expected_uri = 'https://take.net?team=solutions%20lab&person=gabriel'  # noqa: WPS323, E501

        # Act
        result = target.build_resource_query(
            uri,
            {
                'team': 'solutions lab',
                'person': 'gabriel'
            }
        )

        # Assert
        assert result == expected_uri

    @mark.parametrize('id', [None, 'some-id'])
    def test_create_get_command(self, id: str) -> None:
        # Arrange
        uri = '/ping'
        target = self.get_target()

        expected_command = Command('get', '/ping')
        expected_command.id = id

        # Act
        result = target.create_get_command(uri, id)

        # Assert
        if not id:
            expected_command.id = result.id
        assert result == expected_command

    @mark.parametrize('id', [None, 'some-id'])
    def test_create_set_command(self, id: str) -> None:
        # Arrange
        uri = '/ping'
        target = self.get_target()

        expected_command = Command('set', '/ping', None, {})
        expected_command.id = id

        # Act
        result = target.create_set_command(uri, {}, id=id)

        # Assert
        if not id:
            expected_command.id = result.id
        assert result == expected_command

    @mark.parametrize('id', [None, 'some-id'])
    def test_create_merge_command(self, id: str) -> None:
        # Arrange
        uri = '/ping'
        target = self.get_target()

        expected_command = Command('merge', '/ping', None, {})
        expected_command.id = id

        # Act
        result = target.create_merge_command(uri, {}, id=id)

        # Assert
        if not id:
            expected_command.id = result.id
        assert result == expected_command

    @mark.parametrize('id', [None, 'some-id'])
    def test_create_delete_command(self, id: str) -> None:
        # Arrange
        uri = '/ping'
        target = self.get_target()

        expected_command = Command('delete', '/ping')
        expected_command.id = id

        # Act
        result = target.create_delete_command(uri, id)

        # Assert
        if not id:
            expected_command.id = result.id
        assert result == expected_command

    @mark.parametrize('id', [None, 'some-id'])
    @mark.asyncio
    async def test_process_command_async(
        self,
        id: str,
        mocker: MockerFixture
    ) -> None:
        # Arrange
        target = self.get_target(mocker.Mock())

        command = Command('get', '/ping')
        command.id = id

        expected_result = Command(
            'get',
            '/ping',
            resource={},
            status='success'
        )

        target.client.process_command_async = mocker.MagicMock(
            return_value=self.__async_return(expected_result)
        )

        # Act
        result = await target.process_command_async(command)

        # Assert
        if not id:
            expected_result.id = result.id
        assert result == expected_result

    def get_target(self, client=None) -> ExtensionBase:
        return ExtensionBase(client)

    def __async_return(self, result: Any) -> Future:
        fut = Future()
        fut.set_result(result)
        return fut
