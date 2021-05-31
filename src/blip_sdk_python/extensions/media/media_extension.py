from typing import Any, Awaitable

from lime_python.protocol.command import Command
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates

POSTMASTER_MEDIA = 'postmaster@media'


class MediaExtension(ExtensionBase):
    """Extension to handle blip media."""

    def __init__(self, client: Any, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_MEDIA}.{domain}')

    async def get_upload_token_async(
        self,
        secure: bool = None,
        **kwargs
    ) -> Awaitable[Command]:
        """Get token to upload media.

        Args:
            secure (bool): is media secure.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_resource_query(
            UriTemplates.MEDIA_UPLOAD,
            {'secure': secure, **kwargs}
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def refresh_media_async(
        self,
        id: str,
        **kwargs
    ) -> Awaitable[Command]:
        """Refresh an uploaded media.

        Args:
            id (str): the media id
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_uri(UriTemplates.REFRESH_MEDIA, id)
        uri = self.build_resource_query(uri, kwargs)
        return await self.process_command_async(self.create_get_command(uri))
