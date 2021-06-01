from typing import Awaitable
from lime_python.protocol import Command
from .content_type import ContentType
from .uri_templates import UriTemplates
from ...extension_base import ExtensionBase


POSTMASTER_AI = 'postmaster@ai'


class EntitiesExtension(ExtensionBase):
    """Extension to handle Blip Entities Services"""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_entity(self, id: str) -> Awaitable[Command]:
        """Get entity

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

    async def set_entity(self, entity: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.ENTITIES,
                entity,
                ContentType.ENTITY
            )
        )

    async def delete_entity(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.ENTITY, id)
            )
        )

    async def delete_entities(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.ENTITY)
        )

    # Model

    async def get_models(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False
    ) -> Awaitable[Command]:
        models_resource_query = self.build_resource_query(
            UriTemplates.MODELS,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                models_resource_query,
            )
        )

    async def get_model(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.MODEL, id)
            )
        )

    async def get_model_summary(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(UriTemplates.MODELS_SUMMARY)
        )

    async def get_last_trained_or_published_model(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(UriTemplates.LAST_TRAINED_OR_PUBLISH_MODEL)
        )

    async def train_model(self) -> Awaitable[Command]:
        return await self.create_set_command(
            UriTemplates.MODELS,
            {},
            ContentType.MODEL_TRAINING
        )

    async def publish_model(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.MODELS,
                {
                    'id': id
                },
                ContentType.MODEL_PUBLISHING
            )
        )
