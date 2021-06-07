from lime_transport_websocket import WebSocketTransport
from pytest import fixture

from src import Application, ChatExtension, Client, MediaExtension


class TestClient:

    @fixture
    def target(self) -> Client:
        yield Client('127.0.0.1', WebSocketTransport(), Application())

    def test_get_chat_extension(self, target: Client) -> None:
        # Act
        result = target.chat_extension
        result2 = target.chat_extension

        # Assert
        assert isinstance(result, ChatExtension)
        assert result == result2

    def test_get_media_extension(self, target: Client) -> None:
        # Act
        result = target.media_extension
        result2 = target.media_extension

        # Assert
        assert isinstance(result, MediaExtension)
        assert result == result2
