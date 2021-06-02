from typing import Awaitable
from lime_python.protocol import Command
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

POSTMASTER_AI = 'postmaster@ai'


class EntitiesExtension(ExtensionBase):
    """Extension to handle Blip Entities Services."""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_entity(self, id: str) -> Awaitable[Command]:
        """Get entity.

        Args:
            id (str): entity id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(ContentType.ENTITY, id)
            )
        )

    async def get_entities(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        name: str = None
    ) -> Awaitable[Command]:
        """Get all entities.

        Args:
            skip (int): Numbers of entities to be skipped.
            take (int): Numbers of entities to be taked.
            ascending (bool): Sets ascending alphabetical order..
            name (str): name.

        Returns:
            Command: Command response
        """
        entities_resource_query = self.build_resource_query(
            UriTemplates.ENTITIES,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending,
                'name': name
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                entities_resource_query
            )
        )

    async def set_entity(self, entity: dict) -> Awaitable[Command]:
        """Add entity on a base.

        Args:
            entity (dict): Entity to be added

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.ENTITIES,
                entity,
                ContentType.ENTITY
            )
        )

    async def delete_entity(self, id: str) -> Awaitable[Command]:
        """Delete a entity.

        Args:
            id (str): Entity id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.ENTITY, id)
            )
        )

    async def delete_entities(self) -> Awaitable[Command]:
        """Delete all entities.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.ENTITY)
        )
