from typing import Awaitable
from lime_python.protocol import Command

from lime_python.protocol.constants.content_types import ContentTypes
from ..extension_base import ExtensionBase
from .uri_templates import UriTemplates
from .content_type import ContentType

POSTMASTER_AI = 'postmaster@ai'
COLLECTION = 'application/vnd.lime.collection+json'


class AiExtension(ExtensionBase):
    """Extension to handle Blip AI Services"""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    # Intents

    async def get_intent(self, id: str, deep: bool = False) -> Awaitable[Command]:
        """Get a specific intent.

        Args:
            id (str): Unique identifier of the command.
            deep (bool, optional): deep.

        Returns:
            Command: Command response
        """
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
