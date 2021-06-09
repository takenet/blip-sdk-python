from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ....client import Client

POSTMASTER_AI = 'postmaster@ai'


class AiModelExtension(ExtensionBase):
    """Extension to handle Blip Analytics Services."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    # Model

    async def get_models_async(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        **kwargs
    ) -> Command:
        """Search in all trained and/or published models.

        Args:
            skip (int): Number of models to be skipped.
            take (int): Number of model to be take.
            ascending (bool): Sets ascending alphabetical order.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        models_resource_query = self.build_resource_query(
            UriTemplates.MODELS,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending,
                **kwargs
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                models_resource_query,
            )
        )

    async def get_model_async(self, id: str) -> Command:
        """Get specific AI model.

        Args:
            id (str): Model id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.MODEL, id)
            )
        )

    async def get_model_summary_async(self) -> Command:
        """Get model summary.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(UriTemplates.MODELS_SUMMARY)
        )

    async def get_last_trained_or_published_model_async(self) -> Command:
        """Get last trained or published model.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(UriTemplates.LAST_TRAINED_OR_PUBLISH_MODEL)
        )

    async def train_model_async(self) -> Command:
        """Train model.

        Returns:
            Command: Command response
        """
        train_model_command = self.create_set_command(
            UriTemplates.MODELS,
            {},
            ContentType.MODEL_TRAINING
        )

        return await self.process_command_async(train_model_command)

    async def publish_model_async(self, id: str) -> Command:
        """Publish an existing artificial intelligence model.

        Args:
            id (str): model id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.MODELS,
                {
                    'id': id
                },
                ContentType.MODEL_PUBLISHING
            )
        )
