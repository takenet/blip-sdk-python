import asyncio
from lime_python import Message
from lime_transport_websocket import WebSocketTransport
from blip_sdk import ClientBuilder, Receiver

IDENTIFIER = '{{your_identifier}}'
ACCESS_KEY = '{{your_acces_key}}'


async def main_async():

    client = ClientBuilder() \
        .with_identifier(IDENTIFIER) \
        .with_access_key(ACCESS_KEY) \
        .with_transport_factory(lambda: WebSocketTransport()) \
        .with_routing_rule('promiscuous') \
        .build()

    await client.connect_async()
    client.add_message_receiver(Receiver(message_predicate, message_processor))


def message_predicate(message: Message) -> bool:
    return message.type_n != 'application/vnd.lime.chatstate+json'


def message_processor(message: Message) -> None:
    print(message)


loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
