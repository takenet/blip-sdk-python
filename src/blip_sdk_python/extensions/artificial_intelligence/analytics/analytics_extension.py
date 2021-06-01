
from typing import Awaitable, List
from lime_python.protocol import Command
from ...extension_base import ExtensionBase
from .uri_templates import UriTemplates
from .content_type import ContentType

POSTMASTER_AI = 'postmaster@ai'


class AnalyticsExtension(ExtensionBase):
    """Extension to handle Blip Analytics Services"""

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

        Returns:
            Command: Command response
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

         Returns:
            Command: Command response
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
            feedbacks (list, optional): feedback list.
            source (str, optional): analysis source.
            begin_date (str, optional): the begin date of the request.
            end_date (str, optional): the end date of the request.
            min_score (str, optional): min score to be considered.
            max_score (str, optional): max score to be considered.

        Returns:
            Command: Command response
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

    async def set_analysis_feedback(self, id: str, analyses: list) -> Awaitable[Command]:
        """Send feedbacks into analysis.

        Args:
            id (str): Command id
            analyses (dict): analyses 

        Returns:
            Command: Command response
        """
        analyses_feedback_resource = {
            'itemType': ContentType.ANALYSIS_FEEDBACK,
            'items': analyses
        }
        analyses_feedback_command = self.create_set_command(
            self.build_uri(UriTemplates.ANALYSES_FEEDBACK, id=id),
            analyses_feedback_resource,
            ContentType.ANALYSIS_FEEDBACK
        )
        return await self.process_command_async(analyses_feedback_command)

    async def get_analytics(self, id: str = None) -> Awaitable[Command]:
        """Get analytics.

        Args:
            id (str, optional): Unique identifier of the command.

        Returns:
            Command: Command response
        """
        uri = self.build_uri(
            UriTemplates.ANALYTICS_ID,
            id) \
            if id else UriTemplates.ANALYTICS

        return await self.process_command_async(self.create_get_command(uri))

    async def set_analytics(self, confusion_matrix: dict) -> Awaitable[Command]:
        """Create a confusion matrix into your model.

        Args:
            confusion_matrix (dict): Represents a confusion matrix model.

        Returns:
            Command: Command response
        """
        confusion_matrix_resource = self.create_set_command(
            UriTemplates.ANALYTICS,
            confusion_matrix,
            ContentType.CONFUSION_MATRIX
        )

        return await self.process_command_async(confusion_matrix_resource)

    async def delete_analytics(self, id: str) -> Awaitable[Command]:
        """Delete analytics.

        Args:
            id (str): Unique identifier of the command.

        Returns:
            Command: Command response
        """
        delete_analytics_command = self.create_delete_command(
            self.build_uri(UriTemplates.ANALYTICS_ID, id=id)
        )

        self.process_command_async(delete_analytics_command)
