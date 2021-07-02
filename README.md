# blip-sdk-python
> Simple BLiP SDK for Python

**This is a work in progress**

[![wemake-python-styleguide](https://img.shields.io/badge/style-wemake-000000.svg)](https://github.com/wemake-services/wemake-python-styleguide)
[![Build](https://github.com/takenet/blip-sdk-python/actions/workflows/unit-testing.yml/badge.svg)](https://github.com/takenet/blip-sdk-python/actions/workflows/unit-testing.yml)
[![PyPI Publish](https://github.com/takenet/blip-sdk-python/actions/workflows/publish-package.yml/badge.svg)](https://github.com/takenet/blip-sdk-python/actions/workflows/publish-package.yml)
[![PyPI - Downloads](https://img.shields.io/pypi/dm/blip-sdk)](https://pypi.org/project/blip-sdk)
[![PyPI](https://img.shields.io/pypi/v/blip-sdk)](https://pypi.org/project/blip-sdk)
[![PyPI - Python Version](https://img.shields.io/pypi/pyversions/blip-sdk)](https://pypi.org/project/blip-sdk)

--------

Read more about BLiP [here](http://blip.ai/)

### Installing

You should install the `blip-sdk` package to access the BLiP server:

    pip install blip-sdk
    pip install lime-transport-websocket

### Instantiate the BlipSdk Client

You will need an `identifier` and an `access key` to connect a chatbot to **BLiP**. To get them:
- Go to [Painel BLiP](http://portal.blip.ai/) and login;
- Click **Create chatbot**;
- Choose the `Create from scratch` model option;
- Go to **Settings** and click in **Connection Information**;
- Get your bot's `identifier` and `access key`.

In order to instantiate the client use the `ClientBuilder` class informing the `identifier` and `access key`

You can start the client asynchronously or synchronously

> Asynchronously (the recommended way)

```python
import asyncio

from lime_transport_websocket import WebSocketTransport
from blip_sdk import ClientBuilder


async def main_async() -> None:
    # Create a client instance passing the identifier and access key of your chatbot
    client = ClientBuilder() \
        .with_identifier(IDENTIFIER) \
        .with_access_key(ACCESS_KEY) \
        .with_transport_factory(lambda: WebSocketTransport()) \
        .build()

    # Connect with the server asynchronously
    # Connection will occurr via websocket on the 8081 port
    await client.connect_async()
    print('Application started. Press Ctrl + c to stop.')

loop = asyncio.get_event_loop()
loop.run_until_complete(main_async())
loop.run_forever()
```

> Or the sync version (we only recommend for scripts)

```python
from time import sleep
from lime_transport_websocket import WebSocketTransport
from blip_sdk import ClientBuilder


def main() -> None:
    # Create a client instance passing the identifier and access key of your chatbot
    client = ClientBuilder() \
        .with_identifier(IDENTIFIER) \
        .with_access_key(ACCESS_KEY) \
        .with_transport_factory(lambda: WebSocketTransport()) \
        .build()

    # Connect with the server asynchronously
    # Connection will occurr via websocket on the 8081 port
    client.connect()
    print('Application started. Press Ctrl + c to stop.')

main()

while True:
    sleep(1)
```

Each `client` instance represents a server connection and can be reused. To close a connection:

```python
await client.close_async()

# or sync
client.close()
```

### Receiving

All messages sent to the chatbot are redirected to registered `receivers` of messages and notifications. You can define filters to specify which envelopes will be handled by each receiver.
The following example shows how to add a simple message receiver:

```python
client.add_message_receiver(Receiver(True, lambda m: print(m)))
```
The next sample shows how to add a notification receiver with a filter for the `received` event type:

```python
client.add_notification_receiver(Receiver(lambda n: n.event == NotificationEvent.RECEIVED, lambda n: print(n)))
```

It's also possible to use a custom function as a filter:

Example of a message receiver filtering by the originator:

```python
def filter_originator(message: Message) -> bool:
    return message.from_n == '553199990000@0mn.io'

client.add_message_receiver(Receiver(filter_originator, lambda m: print(m)))
```

Each registration of a receiver returns a `handler` that can be used to cancel the registration:

```python
remove_receiver = client.add_message_receiver(Receiver(True, lambda m: print(m)))

remove_receiver()
```

### Sending

It's possible to send notifications and messages only after the session has been stablished.

The following sample shows how to send a message after the connection has been stablished:

```python
await client.connect_async()

# Once connected it's possible to send messages
message = client.send_message(Message('text/plain', 'message', to=user_id))
```

The following sample shows how to send a notification after the connection has been stablished:

```python
client.connect_async()
notification = Notification(
    NotificationEvent.Received,
    Reason(ReasonCode.ApplicationError, 'failed'),
    to=user_Id
)
client.send_notification(notiication)
```

## Contributing

For information on how to contribute to this package, please refer to our [Contribution guidelines](https://github.com/takenet/blip-sdk-js/blob/master/CONTRIBUTING.md).
