from lime_python.protocol import Command
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates


class AiModelExtension(ExtensionBase):
    """Extension to handle Blip Analytics Services."""

    # Model

    async def get_models(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False
    ) -> Command:
        """Get models.

        Args:
            skip (int): Number of models to be skipped.
            take (int): Number of model to be take.
            ascending (bool): Sets ascending alphabetical order.

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

    async def get_model(self, id: str) -> Command:
        """Get model.

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

    async def get_model_summary(self) -> Command:
        """Get model summary.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(UriTemplates.MODELS_SUMMARY)
        )

    async def get_last_trained_or_published_model(self) -> Command:
        """Get last trained or published model.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(UriTemplates.LAST_TRAINED_OR_PUBLISH_MODEL)
        )

    async def train_model(self) -> Command:
        """Train model.

        Returns:
            Command: Command response
        """
        return await self.create_set_command(
            UriTemplates.MODELS,
            {},
            ContentType.MODEL_TRAINING
        )

    async def publish_model(self, id: str) -> Command:
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