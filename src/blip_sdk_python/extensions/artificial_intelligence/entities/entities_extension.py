from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ....client import Client

POSTMASTER_AI = 'postmaster@ai'


class EntitiesExtension(ExtensionBase):
    """Extension to handle Blip Entities Services."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_entity_async(self, id: str) -> Command:
        """Get entity.

        Args:
            id (str): entity id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.ENTITY, id)
            )
        )

    async def get_entities_async(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        name: str = None,
        **kwargs
    ) -> Command:
        """Get all entities.

        Args:
            skip (int): Numbers of entities to be skipped.
            take (int): Numbers of entities to be taked.
            ascending (bool): Sets ascending alphabetical order..
            name (str): name.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        entities_resource_query = self.build_resource_query(
            UriTemplates.ENTITIES,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending,
                'name': name,
                **kwargs
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                entities_resource_query
            )
        )

    async def set_entity_async(self, entity: dict) -> Command:
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

    async def delete_entity_async(self, id: str) -> Command:
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

    async def delete_entities_async(self) -> Command:
        """Delete all entities.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.ENTITIES)
        )
