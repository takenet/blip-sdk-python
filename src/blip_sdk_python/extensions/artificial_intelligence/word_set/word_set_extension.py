from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command, ContentTypes
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ....client import Client

POSTMASTER_AI = 'postmaster@ai'


class WordSetExtension(ExtensionBase):
    """Extension to handle Worsd Set AI Services."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_word_set_async(
        self,
        id: str,
        deep: bool = False,
        **kwargs
    ) -> Command:
        """Get word set.

        Args:
            id (str): word set id
            deep (bool): deep.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        word_set_resource_query = self.build_resource_query(
            self.build_uri(UriTemplates.WORD_SET, id),
            {
                'deep': deep,
                **kwargs
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                word_set_resource_query
            )
        )

    async def set_word_set_resource_async(
        self,
        id: str,
        resource: dict
    ) -> Command:
        """Create word set.

        Args:
            id (str): word set id
            resource (dict): word set resource

        Returns:
            Command: Command response
        """
        set_resource_command = self.create_set_command(
            self.build_uri(UriTemplates.WORD_SET, id),
            type_n=ContentTypes.COLLECTION,
            resource={
                'itemType': ContentType.WORD_SET_WORD,
                'items': resource
            }
        )

        return await self.process_command_async(set_resource_command)

    async def set_word_set_async(self, word_set: dict) -> Command:
        """Create word set.

        Args:
            word_set (dict): word set object

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.WORD_SETS,
                word_set,
                ContentType.WORD_SET
            )
        )

    async def delete_word_set_async(self, id: str) -> Command:
        """Delete word set.

        Args:
            id (str): word set id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.WORD_SET, id)
            )
        )

    async def analyse_word_set_async(self, analysis: dict) -> Command:
        """Analyse word set.

        Args:
            analysis (dict): Analysis

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.WORD_SETS_ANALYSIS,
                analysis,
                ContentType.WORD_SET_ANALYSIS
            )
        )
