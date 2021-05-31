from typing import Awaitable, List
from lime_python.protocol import command

from lime_python.protocol.constants.content_types import ContentTypes
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates
from .content_type import ContentType
from lime_python.protocol.command import Command

POSTMASTER_AI = 'postmaster@ai'
COLLECTION = 'application/vnd.lime.collection+json'


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
            feedbacks (list, optional): feedback list.
            source (str, optional): analysis source.
            begin_date (str, optional): the begin date of the request.
            end_date (str, optional): the end date of the request.
            min_score (str, optional): min score to be considered.
            max_score (str, optional): max score to be considered.

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
            'itemType': ContentType.ANALYSIS_FEEDBACK,
            'items': analyses
        }
        analyses_feedback_command = self.create_set_command(
            self.build_uri(UriTemplates.ANALYSES_FEEDBACK, id=id),
            analyses_feedback_resource,
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
        set_intents_resource = {
            'itemType': ContentType.INTENTION,
            'items': intents
        }
        set_intents_command = self.create_set_command(
            UriTemplates.INTENTIONS,
            set_intents_resource,
            COLLECTION
        )

        return await self.process_command_async(set_intents_command)

    async def merge_intent(self, intent: dict):
        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            intent,
            COLLECTION
        )

        return await self.process_command_async(merge_intents_command)

    async def merge_intents(self, intents: list):
        merge_intents_resource = {
            'itemType': ContentType.INTENTION,
            'items': intents
        }
        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            merge_intents_resource,
            COLLECTION
        )

        return await self.process_command_async(merge_intents_command)

    async def delete_intent(self, id):
        delete_intent_uri = self.build_uri(UriTemplates.INTENTION, id)

        return await self.process_command_async(
            self.create_delete_command(delete_intent_uri)
        )

    async def delete_intents(self):
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.INTENTIONS)
        )

    # Intent Answers

    async def get_intent_answers(
        self,
        id: str,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False
    ) -> Awaitable[Command]:

        intent_answers_query = self.build_resource_query(
            self.build_uri(UriTemplates.INTENTION_ANSWERS, id),
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                intent_answers_query
            )
        )

    async def set_intent_answers(self, id: str, answers: dict):
        intent_answers_command = self.create_set_command(
            self.build_uri(UriTemplates.INTENTION_ANSWERS, id),
            type_n=COLLECTION,
            resource={
                'itemType': ContentType.ANSWER,
                'items': answers
            }
        )

        return await self.process_command_async(intent_answers_command)

    async def delete_intent_answers(self, id: str, answer_id: str):
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.INTENTION_ANSWER, id, answer_id)
            )
        )

    # Intent Questions
    async def get_intent_questions(self, id: str):
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.INTENTION_QUESTIONS, id)
            )
        )

    async def set_intent_questions(self, id: str, questions: list) -> Awaitable[Command]:
        intent_questions_resource = {
            'itemType': ContentType.QUESTION,
            'items': questions
        }
        return await self.process_command_async(
            self.create_set_command(
                self.build_uri(UriTemplates.INTENTION_QUESTIONS, id),
                intent_questions_resource,
                COLLECTION
            )
        )

    async def delete_intent_question(self, id: str, question_id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(
                    UriTemplates.INTENTION_QUESTION,
                    id=id,
                    question_id=question_id
                )
            )
        )

    # Entity

    async def get_entity(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(ContentType.ENTITY, id)
            )
        )

    async def get_entities(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        name: str = None
    ) -> Awaitable[Command]:
        entities_resource_query = self.build_resource_query(
            UriTemplates.ENTITIES,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending,
                'name': name
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                entities_resource_query
            )
        )

    async def set_entity(self, entity: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.ENTITIES,
                entity,
                ContentType.ENTITY
            )
        )

    async def delete_entity(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.ENTITY, id)
            )
        )

    async def delete_entities(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.ENTITY)
        )

    # Model

    async def get_models(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False
    ) -> Awaitable[Command]:
        models_resource_query = self.build_resource_query(
            UriTemplates.MODELS,
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending
            }
        )

    async def get_model(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.MODEL, id)
            )
        )

    async def get_model_summary(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(UriTemplates.MODELS_SUMMARY)
        )

    async def get_last_trained_or_published_model(self) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(UriTemplates.LAST_TRAINED_OR_PUBLISH_MODEL)
        )

    async def train_model(self) -> Awaitable[Command]:
        return await self.create_set_command(
            UriTemplates.MODELS,
            {},
            ContentType.MODEL_TRAINING
        )

    async def publish_model(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.MODELS,
                ContentType.MODEL_PUBLISHING,
                {
                    'id': id
                }
            )
        )

    # Word Set

    async def get_word_set(self, id: str, deep: bool = False) -> Awaitable[Command]:
        word_set_resource_query = self.build_resource_query(
            self.build_uri(UriTemplates.WORD_SET, id),
            {
                'deep': deep
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                word_set_resource_query
            )
        )

    async def set_word_set_resource(self, id: str, resource: dict) -> Awaitable[Command]:
        set_resource_command = self.create_set_command(
            self.build_uri(UriTemplates.WORD_SET_WORD, id),
            type_n=COLLECTION,
            resource={
                'itemType': ContentType.WORD_SET_WORD,
                'items': resource
            }
        )

        return await self.process_command_async(set_resource_command)

    async def set_word_set(self, word_set: any) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.WORD_SETS,
                word_set,
                ContentType.WORD_SET
            )
        )

    async def delete_word_set(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.WORD_SET, id)
            )
        )

    async def analyse_word_set(self, analysis: dict) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.WORD_SETS_ANALYSIS,
                analysis,
                ContentType.WORD_SET_ANALYSIS
            )
        )

    # Content Assistant

    async def analyse_content(self, analysis: dict) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.CONTENT_ANALYSIS,
                analysis,
                ContentType.ANALYSIS
            )
        )

    async def match_content(self, combination: dict) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.CONTENT_ANALYSIS,
                combination,
                ContentType.CONTENT_COMBINATION
            )
        )

    async def get_contents(
        self,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        intents: list = [],
        entities: list = [],
        text: str = '',
        begin_date: str = '',
        end_date: str = ''
    ) -> Awaitable[Command]:

        contents_resource_query = {
            '$skip': skip,
            '$take': take,
            '$ascending': ascending,
            'intents': intents,
            'entities': entities,
            'text': text,
            'beginDate': begin_date,
            'endDate': end_date
        }

        return await self.process_command_async(
            self.create_get_command(contents_resource_query)
        )

    async def get_content(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.CONTENT_ID, id)
            )
        )

    async def set_content(self, content: dict) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.CONTENT,
                content,
                ContentType.CONTENT_RESULT
            )
        )

    async def set_content_result(self, id: str, content: dict) -> Awaitable[Command]:
        content_result_command = self.create_set_command(
            self.build_uri(UriTemplates.CONTENT_ID, id=id),
            content,
            ContentType.CONTENT_RESULT
        )

        return await self.process_command_async(content_result_command)

    async def set_content_combination(self, id: str, combination: dict) -> Awaitable[Command]:
        return self.process_command_async(
            self.create_set_command(
                self.build_uri(UriTemplates.CONTENT_ID, id=id),
                combination,
                ContentType.CONTENT_COMBINATION
            )
        )

    async def set_content_combinations(self, id: str, combinations=list) -> Awaitable[Command]:
        combinations_command = self.create_set_command(
            self.build_uri(UriTemplates.CONTENT_ID, id=id),
            type_n=COLLECTION,
            resource={
                'itemType': ContentType.CONTENT_COMBINATION,
                'items': combinations
            }
        )

        return await self.process_command_async(combinations_command)

    async def delete_content(self, id: str) -> Awaitable[Command]:
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.CONTENT_ID, id)
            )
        )
