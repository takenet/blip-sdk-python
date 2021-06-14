from __future__ import annotations
from dataclasses import dataclass, field
from typing import TYPE_CHECKING

from .ai_analytics import AiAnalyticsExtension
from .ai_model import AiModelExtension
from .content_assistant import ContentAssistantExtension
from .entities import EntitiesExtension
from .intents import IntentsExtension
from .word_set import WordSetExtension

if TYPE_CHECKING:
    from ...client import Client


@dataclass
class AiExtension:
    """AI bundled extensions."""

    client: Client
    to: str
    ai_model: AiModelExtension = field(init=False)
    analytics: AiAnalyticsExtension = field(init=False)
    content_assistant: ContentAssistantExtension = field(init=False)
    entities: EntitiesExtension = field(init=False)
    intents: IntentsExtension = field(init=False)
    word_set: WordSetExtension = field(init=False)

    def __post_init__(self) -> None:  # noqa: D105
        self.ai_model = AiModelExtension(self.client, self.to)
        self.analytics = AiAnalyticsExtension(self.client, self.to)
        self.content_assistant = ContentAssistantExtension(
            self.client,
            self.to
        )
        self.entities = EntitiesExtension(self.client, self.to)
        self.intents = IntentsExtension(self.client, self.to)
        self.word_set = WordSetExtension(self.client, self.to)
