from typing import Any

from lime_python import Command
from ..extension_base import ExtensionBase
from .content_types import ContentTypes
from .uri_templates import UriTemplates


class ChatExtension(ExtensionBase):
    """Extension to handle blip chat history."""

    async def get_threads_async(
        self,
        take: int = None,
        skip: int = None,
        message_date: str = None,
        refresh_expired_media: bool = None,
        **kwargs
    ) -> Command:
        """Get chatbot message history.

        Args:
            take (int):	Limit of total of items to be returned. \
            The maximum value allowed is 100
            skip (int): The number of elements to be skipped
            message_date (str): Initial date on the threads query
            refresh_expired_media (bool): Defines if the expired media \
            links should be refreshed
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_resource_query(
            UriTemplates.THREADS,
            {
                '$take': take,
                '$skip': skip,
                'messageDate': message_date,
                'refreshExpiredMedia': refresh_expired_media,
                **kwargs
            }
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def get_thread_async(
        self,
        identity: str = None,
        take: int = None,
        skip: int = None,
        message_id: str = None,
        storage_date: str = None,
        direction: str = None,
        refresh_expired_media: bool = None,
        decrypt_content: bool = None,
        after: str = None,
        **kwargs
    ) -> Command:
        """Get a user thread message history.

        Args:
            identity (str): user identity
            take (int):	Limit of total of items to be returned. \
            The maximum value allowed is 100
            skip (int): The number of elements to be skipped
            message_id (str): Initial message id for the thread messages query
            storage_date (str): The reference date to search. \
            Example: 2020-01-08T15:59:07.086Z
            direction (str): Possible values: asc and desc. \
            Define whether messages will be returned \
            after(in ascending order) \
            or before(in descending order) a date, respectively. \
            Needs storageDate or messageId to be defined
            refresh_expired_media (bool): Defines if the expired \
            media links should be refreshed
            decrypt_content (bool): decrypt the content
            after (str): after
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: [description]
        """
        uri = self.build_uri(UriTemplates.THREAD, identity)
        uri = self.build_resource_query(
            uri,
            {
                '$take': take,
                '$skip': skip,
                'messageId': message_id,
                'storageDate': storage_date,
                'direction': direction,
                'refreshExpiredMedia': refresh_expired_media,
                'decryptContent': decrypt_content,
                'after': after,
                **kwargs
            }
        )
        return await self.process_command_async(self.create_get_command(uri))

    async def get_thread_unread_messages_async(
        self,
        identity: str,
        **kwargs
    ) -> Command:
        """Get user unread messages.

        Args:
            identity (str): user identity
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command
        """
        uri = self.build_uri(UriTemplates.THREAD_UNREAD_MESSAGES, identity)
        uri = self.build_resource_query(uri, kwargs)
        return await self.process_command_async(self.create_get_command(uri))

    async def set_thread_async(
        self,
        identity: str,
        thread: Any,
        **kwargs
    ) -> Command:
        """Set a user thread.

        Args:
            identity (str): user identity
            thread (Any): message thread
            kwargs: any other optional parameter not covered by the methods

        Returns:
            Command
        """
        uri = self.build_uri(UriTemplates.THREAD, identity)
        uri = self.build_resource_query(uri, kwargs)
        return await self.process_command_async(
            self.create_set_command(uri, thread, ContentTypes.THREAD_MESSAGE)
        )
