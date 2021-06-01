from typing import Awaitable
from lime_python.protocol import Command, ContentTypes, command
from .content_type import ContentType
from .uri_templates import UriTemplates
from ...extension_base import ExtensionBase

POSTMASTER_AI = 'postmaster@ai'


class IntentsExtension(ExtensionBase):
    """Extension to handle Blip AI Services"""

    def __init__(self, client, domain):
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')

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
        """Getting all intents from a model.

        Args:
            skip (int, optional): The number of intents to be skipped.
            take (int, optional): The number of intents to be returned.
            deep (bool, optional): deep.
            name (str, optional): intent name.
            ascending (bool, optional): Sets ascending alphabetical order.

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
                '$ascending': ascending
            }
        )

        return await self.process_command_async(
            self.create_get_command(intents_resource_query)
        )

    async def set_intent(self, intent: dict) -> Awaitable[Command]:
        """Create intent

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

    async def set_intents(self, intents: list) -> Awaitable[Command]:
        """Create list of intents.

        Args:
            intents (list): List of intents

        Returns:
            Command: Response command
        """
        set_intents_resource = {
            'itemType': ContentType.INTENTION,
            'items': intents
        }
        set_intents_command = self.create_set_command(
            UriTemplates.INTENTIONS,
            set_intents_resource,

        )

        return await self.process_command_async(set_intents_command)

    async def merge_intent(self, intent: dict) -> Awaitable[Command]:
        """Merge an intent into a base.

        Args:
            intent (dict): Intent to be merged

        Returns:
            Command: Response command
        """
        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            intent,
            ContentTypes.COLLECTION
        )

        return await self.process_command_async(merge_intents_command)

    async def merge_intents(self, intents: list) -> Awaitable[Command]:
        """Merge list of intents into a base.

        Args:
            intents (list): intents list

        Returns:
            Command: Command response
        """
        merge_intents_resource = {
            'itemType': ContentType.INTENTION,
            'items': intents
        }
        merge_intents_command = self.create_merge_command(
            UriTemplates.INTENTIONS,
            merge_intents_resource,
            ContentTypes.COLLECTION
        )

        return await self.process_command_async(merge_intents_command)

    async def delete_intent(self, id: str) -> Awaitable[Command]:
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

    async def delete_intents(self):
        """Delete all intents from base.

        Returns:
            Command: Command response
        """
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
        """Get intent answers.

        Args:
            id (str): Intent id
            skip (int, optional): Number of answers to be skipped.
            take (int, optional): Number of answers to be take.
            ascending (bool, optional): Sets ascending alphabetical order.

        Returns:
            Command: Command response
        """

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

    async def set_intent_answers(self, id: str, answers: dict) -> Awaitable[Command]:
        """Set a intent answer

        Args:
            id (str): Intent id
            answers (dict): Answer

        Returns:
            Command: Command response
        """
        intent_answers_command = self.create_set_command(
            self.build_uri(UriTemplates.INTENTION_ANSWERS, id),
            type_n=ContentTypes.COLLECTION,
            resource={
                'itemType': ContentType.ANSWER,
                'items': answers
            }
        )

        return await self.process_command_async(intent_answers_command)

    async def delete_intent_answers(self, id: str, answer_id: str) -> Awaitable[Command]:
        """Delete a intent answer

        Args:
            id (str): Intent id
            answer_id (str): Answer id
        Returns:
            Command: Command response
        """
        return await self.process_command_async(
            self.create_delete_command(
                self.build_uri(UriTemplates.INTENTION_ANSWER,
                               id, answerId=answer_id)
            )
        )

    # Intent Questions
    async def get_intent_questions(self, id: str):
        """Get intent questions

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

    async def set_intent_questions(self, id: str, questions: list) -> Awaitable[Command]:
        """Create a intent question

        Args:
            id (str): Intent id
            questions (list): Question

        Returns:
            Command: Command response
        """
        intent_questions_resource = {
            'itemType': ContentType.QUESTION,
            'items': questions
        }
        return await self.process_command_async(
            self.create_set_command(
                self.build_uri(UriTemplates.INTENTION_QUESTIONS, id),
                intent_questions_resource,
                ContentTypes.COLLECTION
            )
        )

    async def delete_intent_question(self, id: str, question_id: str) -> Awaitable[Command]:
        """Delete a intent question

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
                    id=id,
                    questionId=question_id
                )
            )
        )
