from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command
from .content_type import ContentType
from .uri_templates import UriTemplates
from ..extension_base import ExtensionBase

if TYPE_CHECKING:
    from ...client import Client

ANALYTICS_DOMAIN = 'postmaster@analytics'


class AnalyticsExtension(ExtensionBase):
    """Extension to handle Blip event tracks"""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{ANALYTICS_DOMAIN}.{domain}')

    async def get_events_async(self) -> Command:
        """Get all events track.

        Returns:
            Command: Commands response
        """

        return await self.process_command_async(
            self.create_get_command(UriTemplates.EVENTS_TRACK)
        )

    async def get_event_track_async(
        self,
        event: str,
        start_date: str,
        end_date: str,
        take: int = 10,
        **kwargs
    ) -> Command:
        """Get specific event track

        Args:
            event (str): event category name
            start_date (str): start date
            end_date (str): end date
            take (int): Numbers of events to be taken
            kwargs (any): key args.

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
        extras: dict
    ) -> Command:
        """Create an event track

        Args:
            category (str): Event category
            action (str): Event action
            extras (dict): Event extras

        Returns:
            Command: Commands response
        """
        create_event_resource = {
            'category': category,
            'action': action,
            'extras': extras
        }

        create_event_command = self.create_set_command(
            UriTemplates.EVENTS_TRACK,
            create_event_resource,
            ContentType.EVENT_TRACK
        )

        return await self.process_command_async(create_event_command)

    async def get_event_track_details_async(
        self,
        category: str,
        action: str,
        start_date: str,
        end_date: str,
        take: int = 10,
        **kwargs
    ) -> Command:
        """Get event track details

        Args:
            category (str): event category name
            action (str): event action name
            start_date (str): start date
            end_date (str): end date
            take (int): Numbers of events to be taken
            kwargs (any): key args.

        Returns:
            Command: Commands response
        """

        event_command = self.create_get_command(
            self.build_resource_query(
                self.build_uri(UriTemplates.EVENT_CATEGORY,
                               category, action),
                {
                    'startDate': start_date,
                    'endDate': end_date,
                    '$take': take,
                    **kwargs
                }
            )
        )

        return await self.process_command_async(event_command)

    async def delete_event_track_async(
        self,
        category: str
    ) -> Command:
        """Delete a specific event category

        Args:
            category (str): Event category name

        Returns:
            Command: Commands response
        """
        delete_command = self.create_delete_command(
            self.build_uri(UriTemplates.EVENT_TRACK, category)
        )

        return await self.process_command_async(delete_command)
