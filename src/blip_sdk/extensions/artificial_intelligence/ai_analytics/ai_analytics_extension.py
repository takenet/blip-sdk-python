from __future__ import annotations
from typing import List

from lime_python import Command

from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates


class AIAnalyticsExtension(ExtensionBase):
    """Extension to handle Blip AI Analytics Services."""

    async def get_analysis_async(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        filter: str = None,
        intents: List[str] = None,
        feedbacks: list = None,
        source: str = None,
        begin_date: str = None,
        end_date: str = None,
        min_score: str = None,
        max_score: str = None,
        **kwargs
    ) -> Command:
        """Retrieve the history of performed analysis.

        Args:
            skip (int): The number of elements to be skipped.
            take (int): Limit of total of items to be returned.
            ascending (bool): Sets ascending alphabetical order.
            filter (str): request filter options.
            intents (List[str]): List of intents.
            feedbacks (list): the analysis feedback.
            source (str): the source provider.
            begin_date (str): the begin date of the request.
            end_date (str): the end date of the request.
            min_score (str): minimal score.
            max_score (str): maximus score.
            kwargs (any): key args.

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
            'maxScore': max_score,
            **kwargs
        }

        uri = self.build_resource_query(UriTemplates.ANALYSIS, analysis_params)
        get_command = self.create_get_command(uri)

        return await self.process_command_async(get_command)

    async def analyse_async(self, text: str, model_id: str = None) -> Command:
        """Analyzes an user sentence using a published model.

        Args:
            text (str): Input analysis
            model_id (str): Model used to analyse. Defaults to last published.

        Returns:
            Command: Command response
        """
        analysis = {
            'text': text
        }
        if model_id:
            analysis['modelId'] = model_id

        analyse_command = self.create_set_command(
            UriTemplates.ANALYSIS,
            type_n=ContentType.ANALYSIS,
            resource=analysis
        )

        return await self.process_command_async(analyse_command)

    async def send_analysis_by_email_async(
        self,
        email: str,
        filter: str = None,
        intents: list = None,
        feedbacks: list = None,
        source: str = None,
        begin_date: str = None,
        end_date: str = None,
        min_score: str = None,
        max_score: str = None,
        **kwargs
    ) -> Command:
        """Send analysis by email.

        Args:
            email (str): email to be sended
            filter (str): filter OData
            intents (list): list of intents.
            feedbacks (list): feedback list.
            source (str): analysis source.
            begin_date (str): the begin date of the request.
            end_date (str): the end date of the request.
            min_score (str): min score to be considered.
            max_score (str): max score to be considered.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        send_email_resource = {
            'email': email,
            'filter': self.build_resource_query(
                UriTemplates.ANALYSIS,
                {
                    '$filter': filter,
                    'intents': intents,
                    'feedbacks': feedbacks,
                    'source': source,
                    'beginDate': begin_date,
                    'endDate': end_date,
                    'minScore': min_score,
                    'maxScore': max_score,
                    **kwargs
                }
            )
        }
        send_email_command = self.create_set_command(
            UriTemplates.ANALYSIS_EMAIL,
            send_email_resource,
            ContentType.JSON_DOCUMENT
        )

        return await self.process_command_async(send_email_command)

    async def set_analysis_feedback_async(
        self,
        analysis_id: str,
        intent_id: str = None,
        feedback: str = None
    ) -> Command:
        """Send feedbacks into analysis.

        Args:
            feedback (str): feedback type
            analysis_id (str): the analysis id
            intent_id (str): the intent id

        Returns:
            Command: Command response
        """
        uri: str
        resource: dict

        if feedback:
            uri = self.build_uri(
                UriTemplates.ANALYSIS_ID_FEEDBACK,
                analysis_id
            )
            resource = {'feedback': feedback}
        else:
            uri = UriTemplates.ANALYSIS_FEEDBACK
            resource = {'analysisId': analysis_id}

        if intent_id:
            resource.update({'intentionId': intent_id})

        analyses_feedback_command = self.create_set_command(
            uri,
            resource,
            ContentType.ANALYSIS_FEEDBACK
        )
        return await self.process_command_async(analyses_feedback_command)

    async def get_confusion_matrix_async(self, id: str = None) -> Command:
        """Get confusion matrix.

        Args:
            id (str): Unique identifier of the command.

        Returns:
            Command: Command response
        """
        uri = self.build_uri(
            UriTemplates.CONFUSION_MATRIX_ID,
            id
        ) if id else UriTemplates.CONFUSION_MATRIX

        return await self.process_command_async(self.create_get_command(uri))

    async def set_confusion_matrix_async(
        self,
        confusion_matrix: dict
    ) -> Command:
        """Create a confusion matrix into your model.

        Args:
            confusion_matrix (dict): Represents a confusion matrix model.

        Returns:
            Command: Command response
        """
        confusion_matrix_resource = self.create_set_command(
            UriTemplates.CONFUSION_MATRIX,
            confusion_matrix,
            ContentType.CONFUSION_MATRIX
        )

        return await self.process_command_async(confusion_matrix_resource)

    async def delete_confusion_matrix_async(self, id: str) -> Command:
        """Delete confusion matrix.

        Args:
            id (str): Confusion matrix id

        Returns:
            Command: Command response
        """
        delete_analytics_command = self.create_delete_command(
            self.build_uri(UriTemplates.CONFUSION_MATRIX_ID, id)
        )

        return await self.process_command_async(delete_analytics_command)
