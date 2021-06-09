from lime_python import Command
from pytest import fixture, mark
from pytest_mock import MockerFixture
from src import EntitiesExtension
from ....async_mock import async_return

AI_TO = 'postmaster@ai.msging.net'


class TestEntitiesExtension:

    @fixture
    def target(self, mocker: MockerFixture) -> EntitiesExtension:
        yield EntitiesExtension(mocker.MagicMock(), 'msging.net')

    @mark.asyncio
    async def test_get_entity_async(
        self,
        mocker: MockerFixture,
        target: EntitiesExtension
    ) -> None:
        # Arrange
        entitie_id = '1234'
        expected_command = Command(
            'get',
            f'/entities/{entitie_id}'
        )

        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.get_entity_async(entitie_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_set_entity_async(
        self,
        mocker: MockerFixture,
        target: EntitiesExtension
    ) -> None:
        # Arrange
        entity_resource = {
            'name': 'Flavor',
            'values': [
                {
                    'name': 'Pepperoni',
                    'synonymous': [
                        'Peperoni',
                        'Pepperonee',
                        'Pepperouni',
                        'Peperony'
                    ]
                },
                {
                    'name': 'Mushrooms',
                    'synonymous': [
                        'Mashrooms',
                        'Mushroom',
                        'Mshrooms'
                    ]
                }
            ]
        }
        expected_command = Command(
            'set',
            '/entities',
            'application/vnd.iris.ai.entity+json',
            entity_resource
        )
        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.set_entity_async(entity_resource)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_entity(
        self,
        mocker: MockerFixture,
        target: EntitiesExtension
    ) -> None:
        # Arrange
        entitie_id = '1234'
        expected_command = Command(
            'delete',
            f'/entities/{entitie_id}'
        )

        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.delete_entity_async(entitie_id)

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)

    @mark.asyncio
    async def test_delete_entities(
        self,
        mocker: MockerFixture,
        target: EntitiesExtension
    ) -> None:
        # Arrange
        expected_command = Command(
            'delete',
            '/entities'
        )

        expected_command.to = AI_TO
        mock = mocker.MagicMock(
            return_value=async_return(None)
        )

        target.client.process_command_async = mock

        # Act
        await target.delete_entities_async()

        # Assert
        expected_command.id = mock.call_args[0][0].id
        mock.assert_called_once_with(expected_command)
