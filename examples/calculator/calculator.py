import asyncio
import re

from lime_python import Command, Identity, Message
from lime_transport_websocket import WebSocketTransport

from blip_sdk import ClientBuilder, Receiver

IDENTIFIER = 'botnotificacaoworkchat'
ACCESS_KEY = 'aGlhYmVFd3VWRThXV1hzNWJxYW0='
CALCULUS_PATTERN = '^[0-9]+(\s)?(\/|\+|-|\*)(\s)?[0-9]+$'

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


def message_predicate(message: Message) -> bool:
    return message.type_n != 'application/vnd.lime.chatstate+json'


async def message_processor_async(message: Message) -> None:
    user_id = Identity.parse_str(message.from_n)
    user_state = await get_context_async(user_id, 'user-state')
    try:
        if is_in_pattern(message.content):
            await calculates_response_async(message.content, user_id)
        elif user_state in ['no_content', '0']:
            await calculator_menu_async(user_id)
        else:
            exception(user_id, message.content)
    except:
        unexpected_error(user_id)


def exception(user_id: Identity, message: str):
    message_content = 'Sorry, i didnt understand,\
         can you enter the problem in the following pattern?: 5 * 2'
    send_message_with_composing(
        user_id,
        'text/plain',
        message_content
    )


async def calculator_menu_async(user_id: Identity):
    send_message_with_composing(
        user_id,
        'text/plain',
        'Enter a problem using the following pattern:\n\
        - x * y for multiplication\n\
        - x / y for division\n\
        - x + y for sum\n\
        - x - y for subtraction'
    )
    await set_context_async(user_id, 'text/plain', 'user-state', '1')


def send_message_with_composing(
    user_id: Identity,
    message_type: str,
    message_content: str
):
    client.send_message(Message(
        to=user_id,
        type_n='application/vnd.lime.collection+json',
        content={
            'itemType': 'application/vnd.lime.container+json',
            'items': [
                {
                    'type': 'application/vnd.lime.chatstate+json',
                    'value': {
                        'state': 'composing'
                    },
                },
                {
                    'type': 'application/vnd.lime.chatstate+json',
                    'value': {
                        'state': 'paused'
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
    return 'no_content'


def is_in_pattern(message_content: str) -> bool:
    return re.search(CALCULUS_PATTERN, message_content)


async def calculates_response_async(message_content: str, user_id: Identity) -> None:
    response = eval(message_content)
    send_message_with_composing(
        user_id=user_id,
        message_type='text/plain',
        message_content=f'The response is {response}'
    )
    await set_context_async(user_id, 'text/plain', 'user-state', '0')


def unexpected_error(user_id: Identity) -> None:
    message_content = 'Sorry, an unexpected error ocurred\
                       can you send a new message?'
    try:
        send_message_with_composing(
            user_id,
            'text/plain',
            message_content
        )
    except:
        raise ValueError('An error ocurred while sending message')


loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
