from typing import Awaitable
from lime_python.protocol import Command
from .content_type import ContentType
from ...extension_base import ExtensionBase
from .uri_templates import UriTemplates


class AiModelExtension(ExtensionBase):
    """Extension to handle Blip Analytics Services"""

    # Model

    async def get_models(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False
    ) -> Awaitable[Command]:
        """Get models

        Args:
            skip (int, optional): Number of models to be skipped. 
            take (int, optional): Number of model to be take.
            ascending (bool, optional): Sets ascending alphabetical order.

        Returns:
            Command: Command response
        """
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
