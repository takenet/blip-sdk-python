from typing import Awaitable, List
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
            'begin_date': begin_date,
            'end_date': end_date,
            'min_score': min_score,
            'max_score': max_score
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
        email_and_filter: str,
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
