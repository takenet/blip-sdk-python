import asyncio
from lime_python import Message
from lime_transport_websocket import WebSocketTransport
from src import ClientBuilder
from src.blip_sdk.receiver import Receiver

IDENTIFIER = 'botnotificacaoworkchat'
ACCESS_KEY = 'aGlhYmVFd3VWRThXV1hzNWJxYW0='


async def main_async():

    client = ClientBuilder() \
        .with_identifier(IDENTIFIER) \
        .with_access_key(ACCESS_KEY) \
        .with_transport_factory(lambda: WebSocketTransport()) \
        .with_routing_rule('promiscuous') \
        .build()

    await client.connect_async()
    print('20')
    client.add_message_receiver(Receiver(True, message_processor))


def message_processor(message: Message) -> None:
    if message.type_n != 'application/vnd.lime.chatstate+json':
        return message


loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
