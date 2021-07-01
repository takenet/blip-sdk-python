import asyncio
from lime_python import Message, Identity
from lime_python.protocol.command import Command
from lime_transport_websocket import WebSocketTransport
from blip_sdk import ClientBuilder, Receiver

IDENTIFIER = 'botnotificacaoworkchat'
ACCESS_KEY = 'aGlhYmVFd3VWRThXV1hzNWJxYW0='

client = ClientBuilder() \
    .with_identifier(IDENTIFIER) \
    .with_access_key(ACCESS_KEY) \
    .with_transport_factory(lambda: WebSocketTransport()) \
    .build()


async def main_async():

    await client.connect_async()
    client.add_message_receiver(
        Receiver(message_predicate, message_processor_async)
    )
    client.add_message_receiver(
        Receiver(message_predicate, message_processor)
    )
    client.add_message_receiver(
        Receiver(message_predicate, message_processor)
    )


def message_predicate(message: Message) -> bool:
    return message.type_n != 'application/vnd.lime.chatstate+json'


def message_processor(message: Message) -> None:
    print(message)


async def message_processor_async(message: Message) -> None:
    user_id = Identity.parse_str(message.from_n)
    user_state = await get_context_async(user_id, 'user-state')
    print(user_state)
    if user_state == 'no_content' or user_state == '0':
        await calculator_menu_async(user_id)
    if isinstance(message.content, int):
        print('a')
    else:
        exception(user_id, message.content)


def exception(user_id: Identity, message: str):
    message_content = 'Desculpe, não entendi, pode digitar novamento por favor?'
    send_message_with_composing(
        user_id,
        'text/plain',
        message_content
    )


async def calculator_menu_async(user_id: Identity):
    client.send_message(
        Message(
            'text/plain',
            '''Digite apenas a operação a ser realizada, utilizando (*) para multiplicação, (/) para divisão
            (-) para subtração e (+) para soma''',
            to=user_id
        )
    )
    await set_context_async(user_id, 'text/plain', 'user-state', '1')


def send_message_with_composing(user_id: Identity, message_type: str, message_content: str):
    client.send_message(Message(
        to=user_id,
        type_n='application/vnd.lime.collection+json',
        content={
            'itemType': 'application/vnd.lime.container+json',
            'items': [
                {
                    'type': 'application/vnd.lime.chatstate+json',
                    'value': {
                        'state': 'composing',
                        'interval': 1000
                    },
                },
                {
                    'type': message_type,
                    'value': message_content
                }
            ]
        }))


async def set_context_async(
    user_id: Identity,
    variable_type: str,
    variable_name: str,
    value: str
) -> None:
    set_context_body = Command(
        'set',
        f'/contexts/{user_id}/{variable_name}',
        variable_type,
        resource=value
    )
    await client.process_command_async(set_context_body)


async def get_context_async(
    user_id: Identity,
    variable_name: str
) -> str:
    get_context_body = Command(
        'get',
        f'/contexts/{user_id}/{variable_name}',
    )
    user_context = await client.process_command_async(get_context_body)
    if user_context.status == 'success':
        return user_context.resource
    else:
        return 'no_content'


loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
