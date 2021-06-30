import asyncio
import time
from lime_python import Message
from lime_python.protocol.command import Command
from lime_transport_websocket import WebSocketTransport
from blip_sdk import ClientBuilder, Receiver

IDENTIFIER = 'botnotificacaoworkchat'
ACCESS_KEY = 'aGlhYmVFd3VWRThXV1hzNWJxYW0='

client = ClientBuilder() \
    .with_identifier(IDENTIFIER) \
    .with_access_key(ACCESS_KEY) \
    .with_transport_factory(lambda: WebSocketTransport()) \
    .with_routing_rule('promiscuous') \
    .build()


async def main_async():

    await client.connect_async()
    client.add_message_receiver(Receiver(message_predicate, message_processor))


def message_predicate(message: Message) -> bool:
    return message.type_n != 'application/vnd.lime.chatstate+json'


def message_processor(message: Message) -> None:
    user_id = get_user_id(message.from_n)
    user_state = get_context(user_id, 'user_state')
    if(user_state == 'no_content' or user_state == 0):
        calculator_menu(user_id)
    if isinstance(message.content, int):
        print('a')
    else:
        exception(user_id, message.content)


def exception(user_id: str, message: str):
    message_content = 'Desculpe, não entendi, pode digitar novamento por favor?'
    send_message_with_composing(
        user_id,
        'text/plain',
        message_content
    )


def calculator_menu(user_id: str):
    client.send_message(
        Message(
            'text/plain',
            'Digite apenas a operação a ser realizada, utilizando (*) para multiplicação, (/) para divisão' +
            ' (-) para subtração e (+) para soma'
        )
    )
    set_context(user_id, 'text/plain', 'user_state', '1')


def send_message_with_composing(user_id: str, message_type: str, message_content: str):
    client.send_message(Message(
        to=user_id,
        type_n='application/vnd.lime.collection+json',
        content={
            'itemType': 'application/vnd.lime.container+json',
            'items': [
                {
                    'type': 'application/vnd.lime.chatstate+json',
                    'value':
                    {
                        'state': 'composing'
                    },
                },
                {
                    'type': message_type,
                    'value': message_content
                }
            ]
        }))


def set_context(
    user_id: str,
    variable_type: str,
    variable_name: str,
    value: str
) -> None:
    set_context_body = Command(
        'set',
        f'/context/{user_id}/{variable_name}',
        variable_type,
        resource=value
    )
    client.process_command(set_context_body)


def get_context(
    user_id: str,
    variable_name: str
) -> str:
    get_context_body = Command(
        'get',
        f'/context/{user_id}/{variable_name}',
    )
    user_context = client.process_command(get_context_body)
    if user_context['status'] == 'success':
        return user_context['resource']
    else:
        return 'no content'


def get_user_id(user_id) -> str:
    return user_id.replace('/deault', '')


loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
