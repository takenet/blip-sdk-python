from asyncio import Future
from time import sleep
from typing import Any, Awaitable


def async_return(result: Any, delay: float = None) -> Awaitable[Any]:
    """Create an async return.

    Args:
        result (Any): the mock result
        delay (float): delay before set result

    Returns:
        Any: the async result response
    """
    fut = Future()
    if delay:
        sleep(delay)
    fut.set_result(result)
    return fut
