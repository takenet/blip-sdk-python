from __future__ import annotations
from typing import TYPE_CHECKING
from lime_python import Command, ContentTypes
from ...extension_base import ExtensionBase
from .content_type import ContentType
from .uri_templates import UriTemplates

if TYPE_CHECKING:
    from ....client import Client

POSTMASTER_AI = 'postmaster@ai'


class IntentsExtension(ExtensionBase):
    """Extension to handle Blip AI Services."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

    async def get_intent_async(
        self,
        id: str,
        deep: bool = False,
        **kwargs
    ) -> Command:
        """Get a specific intent.

        Args:
            id (str): Unique identifier of the command.
            deep (bool): deep.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        get_intent_command = self.create_get_command(
            self.build_resource_query(
                self.build_uri(UriTemplates.INTENTION, id),
                {
                    'deep': deep,
                    **kwargs
                }
            )
        )

        return await self.process_command_async(get_intent_command)

    async def get_intents_async(
        self,
        skip: int = 0,
        take: int = 100,
        deep: bool = False,
        name: str = None,
        ascending: bool = False,
        **kwargs
    ) -> Command:
        """Get all intents from a model.

        Args:
            skip (int): The number of intents to be skipped.
            take (int): The number of intents to be returned.
            deep (bool): deep.
            name (str): intent name.
            ascending (bool): Sets ascending alphabetical order.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        intents_resource_query = self.build_resource_query(
            UriTemplates.INTENTIONS,
            {
                '$skip': skip,
                '$take': take,
                'deep': deep,
                'name': name,
                '$ascending': ascending,
                **kwargs
            }
        )

        return await self.process_command_async(
            self.create_get_command(intents_resource_query)
        )

    async def set_intent_async(self, intent: dict) -> Command:
        """Create intent.

        Args:
            intent (dict): intent object

        Returns:
            Command: Response Command
        """
        return await self.process_command_async(
            self.create_set_command(
                UriTemplates.INTENTIONS,
                intent,
                ContentType.INTENTION
            )
        )

    async def set_intents_async(self, intents: list) -> Command:
        """Create list of intents.

        Args:
            intents (list): List of intents

        Returns:
            Command: Response command
        """
        set_intents_resource = self.__build_resource(
            intents,
            ContentType.INTENTION
        )

        set_intents_command = self.create_set_command(
            UriTemplates.INTENTIONS,
            set_intents_resource,
            ContentTypes.COLLECTION
        )

        return await self.process_command_async(set_intents_command)

    async def merge_intent_async(self, intent: dict) -> Command:
        """Merge an intent into a base.

        Args:
            intent (dict): Intent to be merged

        Returns:
            Command: Response command
        """
        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            intent,
            ContentType.INTENTION
        )

        return await self.process_command_async(merge_intents_command)

    async def merge_intents_async(self, intents: list) -> Command:
        """Merge list of intents into a base.

        Args:
            intents (list): intents list

        Returns:
            Command: Command response
        """
        merge_intents_resource = self.__build_resource(
            intents,
            ContentType.INTENTION
        )

        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            merge_intents_resource,
            ContentTypes.COLLECTION
        )

        return await self.process_command_async(merge_intents_command)

    async def delete_intent_async(self, id: str) -> Command:
        """Delete intent from base.

        Args:
            id (str): Intent identifier

        Returns:
            Command: Command response
        """
        delete_intent_uri = self.build_uri(UriTemplates.INTENTION, id)

        return await self.process_command_async(
            self.create_delete_command(delete_intent_uri)
        )

    async def delete_intents_async(self):
        """Delete all intents from base.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(UriTemplates.INTENTIONS)
        )

    # Intent Answers

    async def get_intent_answers_async(
        self,
        id: str,
        skip: int = 0,
        take: int = 100,
        ascending: bool = False,
        **kwargs
    ) -> Command:
        """Get intent answers.

        Args:
            id (str): Intent id
            skip (int): Number of answers to be skipped.
            take (int): Number of answers to be take.
            ascending (bool): Sets ascending alphabetical order.
            kwargs: any other optional parameter not covered by the method

        Returns:
            Command: Command response
        """
        intent_answers_query = self.build_resource_query(
            self.build_uri(UriTemplates.INTENTION_ANSWERS, id),
            {
                '$skip': skip,
                '$take': take,
                '$ascending': ascending,
                **kwargs
            }
        )

        return await self.process_command_async(
            self.create_get_command(
                intent_answers_query
            )
        )

    async def set_intent_answers_async(
        self,
        id: str,
        answers: list
    ) -> Command:
        """Set a intent answer.

        Args:
            id (str): Intent id
            answers (list): Answers list

        Returns:
            Command: Command response
        """
        intent_answers_command = self.create_set_command(
            self.build_uri(UriTemplates.INTENTION_ANSWERS, id),
            type_n=ContentTypes.COLLECTION,
            resource=self.__build_resource(
                answers,
                ContentType.ANSWER
            )
        )

        return await self.process_command_async(intent_answers_command)

    async def delete_intent_answers_async(
        self,
        id: str,
        answer_id: str
    ) -> Command:
        """Delete intent answer.

        Args:
            id (str): intent id.
            answer_id (str): answer id.

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(
                    UriTemplates.INTENTION_ANSWER,
                    id,
                    answer_id
                )
            )
        )

    # Intent Questions
    async def get_intent_questions_async(self, id: str):
        """Get intent questions.

        Args:
            id (str): Intent id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_get_command(
                self.build_uri(UriTemplates.INTENTION_QUESTIONS, id)
            )
        )

    async def set_intent_questions_async(
        self,
        id: str,
        questions: list
    ) -> Command:
        """Create a intent question.

        Args:
            id (str): Intent id
            questions (list): Question

        Returns:
            Command: Command response
        """
        intent_questions_resource = self.__build_resource(
            questions,
            ContentType.QUESTION
        )

        return await self.process_command_async(
            self.create_set_command(
                self.build_uri(UriTemplates.INTENTION_QUESTIONS, id),
                intent_questions_resource,
                ContentTypes.COLLECTION
            )
        )

    async def delete_intent_question_async(
        self,
        id: str,
        question_id: str
    ) -> Command:
        """Delete a intent question.

        Args:
            id (str): Intent id
            question_id (str): Question id

        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(
                    UriTemplates.INTENTION_QUESTION,
                    id,
                    question_id
                )
            )
        )

    def __build_resource(self, items: list, item_type: str) -> dict:
        return {
            'itemType': item_type,
            'items': items
        }
