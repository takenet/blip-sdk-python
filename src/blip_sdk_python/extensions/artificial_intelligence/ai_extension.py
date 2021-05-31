from typing import Awaitable, List

from lime_python.protocol.constants.content_types import ContentTypes
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates
from .content_type import ContentType
from lime_python.protocol.command import Command

POSTMASTER_AI = 'postmaster@ai'


class AiExtension(ExtensionBase):
    """Extension to handle Blip AI Services"""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_analysis(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        filter: str = None,
        intents: List[str] = [],
        feedbacks: list = [],
        source: str = None,
        begin_date: str = None,
        end_date: str = None,
        min_score: str = None,
        max_score: str = None,
        **kwargs
    ) -> Awaitable[Command]:
        """Retrieves the history of performed analysis.
        Args:
            skip (int, optional): The number of elements to be skipped.
            take (int, optional): Limit of total of items to be returned.
            ascending (bool, optional): Sets ascending alphabetical order.
            filter (str, optional): request filter options.
            intents (List[str], optional): List of intents.
            feedbacks (List, optional): the analysis feedback.
            source (str, optional): the source provider.
            begin_date (str, optional): the begin date of the request.
            end_date (str, optional): the end date of the request.
            min_score (str, optional): minimal score.
            max_score (str, optional): maximus score.
        """

        analysis_params = {
            '$skip': skip,
            '$take': take,
            '$ascending': ascending,
            '$filter': filter,
            'intents': intents,
            'feedbaccks': feedbacks,
            'source': source,
            'beginDate': begin_date,
            'endDate': end_date,
            'minScore': min_score,
            'maxScore': max_score
        }

        query_params = {**analysis_params, **kwargs}
        uri = self.build_resource_query(UriTemplates.ANALYSIS, query_params)
        get_command = self.create_get_command(uri)

        return await self.process_command_async(get_command)

    def analyse(self, analysis: dict) -> Command:
        """Analyzes an user sentence using a published model.

        Args:
            analysis (dict): Input analysis
        """
        self.create_set_command(
            UriTemplates.ANALYSIS,
            type_n=ContentType.ANALYSIS,
            resource=analysis
        )

    async def set_analysis_by_email(
        self,
        email_and_filter: dict,
        intents: list = [],
        feedbacks: list = [],
        source: str = None,
        begin_date: str = None,
        end_date: str = None,
        min_score: str = None,
        max_score: str = None
    ) -> Awaitable[Command]:
        """[summary]

        Args:
            email_and_filter (str): email and filter
            intents (list, optional): list of intents.
            feedbacks (list, optional): [description].
            source (str, optional): [description].
            begin_date (str, optional): [description].
            end_date (str, optional): [description].
            min_score (str, optional): [description].
            max_score (str, optional): [description].

        Returns:
            Awaitable[Command]: Command response
        """
        send_email_resource = {
            'email': email_and_filter['email'],
            'filter': self.build_resource_query(
                UriTemplates.ANALYSIS,
                {
                    '$filter': email_and_filter['filter'],
                    'intents': intents,
                    'feedbacks': feedbacks,
                    'source': source,
                    'beginDate': begin_date,
                    'endDate': end_date,
                    'minScore': min_score,
                    'maxScore': max_score
                }
            )
        }
        send_email_command = self.create_set_command(
            UriTemplates.ANALYSIS_EMAIL,
            send_email_resource,
            ContentType.JSON_DOCUMENT
        )

        return await self.process_command_async(send_email_command)

    async def set_analysis_feedback(self, id: str, analyses: dict):
        analyses_feedback_resource = {
            'item_type': ContentType.ANALYSIS_FEEDBACK,
            'items': analyses
        }
        analyses_feedback_command = self.create_set_command(
            self.build_uri(UriTemplates.ANALYSES_FEEDBACK, id=id),
            analyses,
            ContentType.ANALYSIS_FEEDBACK
        )
        return await self.process_command_async(analyses_feedback_command)

    # analytics
    async def get_analytics(self, id: str = None):
        uri = self.build_uri(
            UriTemplates.ANALYTICS_ID,
            id) \
            if id else UriTemplates.ANALYTICS

        return await self.process_command_async(self.create_get_command(uri))

    async def set_analytics(self, confusion_matrix):
        confusion_matrix_resource = self.create_set_command(
            UriTemplates.ANALYTICS,
            ContentType.CONFUSION_MATRIX,
            confusion_matrix
        )

        return await self.process_command_async(confusion_matrix_resource)

    async def delete_analytics(self, id: str):
        delete_analytics_command = self.create_delete_command(
            self.build_uri(UriTemplates.ANALYTICS_ID, id)
        )

        self.process_command_async(delete_analytics_command)

    # Intents

    async def get_intent(self, id: str, deep: bool = False):
        get_intent_command = self.create_get_command(
            self.build_resource_query(
                self.build_uri(UriTemplates.INTENTION, id),
                {
                    'deep': deep
                }
            )
        )

        return await self.process_command_async(get_intent_command)

    async def get_intents(
        self,
        skip: int = 0,
        take: int = 100,
        deep: bool = False,
        name: str = None,
        ascending: bool = False
    ) -> Awaitable[Command]:

        intents_resource_query = self.build_resource_query(
            UriTemplates.INTENTIONS,
            {
                '$skip': skip,
                '$take': take,
                'deep': deep,
                'name': name,
                '$ascending': ascending
            }
        )

        return await self.process_command_async(
            self.create_get_command(intents_resource_query)
        )

    async def set_intent(self, intent: dict) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.INTENTIONS,
                intent,
                ContentType.INTENTION
            )
        )

    async def set_intents(self, intents: list) -> Awaitable[Command]:
        set_intents_command = self.create_set_command(
            UriTemplates.INTENTIONS,
            ContentType
        )
