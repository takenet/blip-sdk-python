from __future__ import annotations

from typing import TYPE_CHECKING

from lime_python import Command
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ...client import Client

POSTMASTER_MEDIA = 'postmaster@media'


class MediaExtension(ExtensionBase):
    """Extension to handle blip media."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_MEDIA}.{domain}')

    async def get_upload_token_async(
        self,
        secure: bool = None,
        **kwargs
    ) -> Command:
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
    ) -> Command:
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
