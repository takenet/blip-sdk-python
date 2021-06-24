from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command
from ..extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ...client import Client

POSTMASTER_ANALYTICS = 'postmaster@analytics'


class AnalyticsExtension(ExtensionBase):
    """Extension to handle Blip event tracks."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_ANALYTICS}.{domain}')

    async def get_categories_async(
        self,
        skip: int = None,
        take: int = None,
        **kwargs
    ) -> Command:
        """Get all bot categories.

        Args:
            skip (int): Number of events to be skipped
            take (int): Number of events to be taken
            kwargs: any other optional parameter not covered by the method.

        Returns:
            Command: Commands response
        """
        return await self.process_command_async(
            self.create_get_command(
                self.build_resource_query(
                    UriTemplates.EVENTS_TRACK,
                    {
                        '$skip': skip,
                        '$take': take,
                        **kwargs
                    }
                )
            )
        )

    async def get_category_actions_counter_async(
        self,
        event: str,
        start_date: str = None,
        end_date: str = None,
        take: int = None,
        **kwargs
    ) -> Command:
        """Get actions counter of a specified event category.

        Args:
            event (str): event category name
            start_date (str): start date
            end_date (str): end date
            take (int): Numbers of events to be taken
            kwargs: any other optional parameter not covered by the method.

        Returns:
            Command: Commands response
        """
        event_command = self.create_get_command(
            self.build_resource_query(
                self.build_uri(UriTemplates.EVENT_TRACK, event),
                {
                    'startDate': start_date,
                    'endDate': end_date,
                    '$take': take,
                    **kwargs
                }
            )
        )

        return await self.process_command_async(event_command)

    async def create_event_track_async(
        self,
        category: str,
        action: str,
        identity: str = None,
        extras: dict = None
    ) -> Command:
        """Create an event track.

        Args:
            category (str): Event category
            action (str): Event action
            identity (str): User identity
            extras (dict): Event extras

        Returns:
            Command: Commands response
        """
        create_event_resource = {
            'category': category,
            'action': action,
            'extras': extras
        }

        if identity is not None:
            create_event_resource['contact'] = {
                'identity': identity
            }

        create_event_command = self.create_set_command(
            UriTemplates.EVENTS_TRACK,
            create_event_resource,
            ContentType.EVENT_TRACK
        )

        return await self.process_command_async(create_event_command)

    async def get_event_details_async(
        self,
        category: str,
        action: str,
        start_date: str = None,
        end_date: str = None,
        take: int = None,
        **kwargs
    ) -> Command:
        """Get all details of an event (event extras for instance).

        Args:
            category (str): event category name
            action (str): event action name
            start_date (str): start date
            end_date (str): end date
            take (int): Numbers of events to be taken
            kwargs: any other optional parameter not covered by the method.

        Returns:
            Command: Commands response
        """
        event_command = self.create_get_command(
            self.build_resource_query(
                self.build_uri(UriTemplates.EVENT_CATEGORY, category, action),
                {
                    'startDate': start_date,
                    'endDate': end_date,
                    '$take': take,
                    **kwargs
                }
            )
        )

        return await self.process_command_async(event_command)

    async def delete_category_async(
        self,
        category: str
    ) -> Command:
        """Delete a specific event category.

        Args:
            category (str): Event category name

        Returns:
            Command: Commands response
        """
        delete_command = self.create_delete_command(
            self.build_uri(UriTemplates.EVENT_TRACK, category)
        )

        return await self.process_command_async(delete_command)
