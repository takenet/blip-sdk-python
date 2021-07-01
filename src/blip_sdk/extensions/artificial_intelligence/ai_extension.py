from __future__ import annotations
from typing import TYPE_CHECKING

from .ai_analytics import AIAnalyticsExtension
from .ai_model import AIModelExtension
from .content_assistant import ContentAssistantExtension
from .entities import EntitiesExtension
from .intents import IntentsExtension
from .word_set import WordSetExtension

if TYPE_CHECKING:
    from ...client import Client

POSTMASTER_AI = 'postmaster@ai'


class AIExtension(
    AIAnalyticsExtension,
    AIModelExtension,
    ContentAssistantExtension,
    EntitiesExtension,
    IntentsExtension,
    WordSetExtension
):
    """AI bundled extensions."""

    def __init__(self, client: Client, domain: str) -> None:
        super().__init__(client, f'{POSTMASTER_AI}.{domain}')
